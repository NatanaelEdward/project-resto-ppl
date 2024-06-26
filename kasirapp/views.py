from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.http import FileResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from django.db.models import ExpressionWrapper, DecimalField, Sum, F
from menuapp.models import PenjualanDetail,PenjualanFaktur,HargaMenu,DataMenu,ProfitSummary,BahanMenu
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.decorators import login_required
from app.decorators import role_required
import requests
from decimal import Decimal
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.
@login_required
@role_required(allowed_roles=('kasir','admin'))
def generate_pdf(request, order_id):
    # Get the PenjualanFaktur instance
    order = get_object_or_404(PenjualanFaktur, id=order_id)

    # Fetch related PenjualanDetail items for the order
    order.menu_items = PenjualanDetail.objects.filter(nomor_nota_penjualan=order.nomor_nota_penjualan)

    # Create a BytesIO buffer to receive the PDF data
    buffer = BytesIO()

    # Create the PDF object, using the BytesIO buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=landscape(letter))

    # Set a large enough page size
    width, height = landscape(letter)
    p.setPageSize((width, height))

    # Define content to print
    content = [
        f'FAKTUR PENJUALAN',
        f'Nomor Nota Penjualan: {order.kode_penjualan_faktur}',
        f'Meja: {order.nomor_meja}',
        f'Tanggal Penjualan: {order.tanggal_penjualan.strftime("%d %b, %Y %I:%M %p")}',
        f'Menu : '
    ]

    # Set the Y-coordinate for the first line of content
    y = height - 100

    # Add content to the PDF
    for line in content:
        p.drawString(100, y, line)
        y -= 20  # Adjust the Y-coordinate for the next line

    # Add menu items to the PDF
    for item in order.menu_items:
        # Get the related HargaMenu based on the harga_menu attribute
        harga_menu = HargaMenu.objects.get(menu=item.kode_menu, harga_menu=item.harga_menu)
        menu_description = f'{item.qty_menu}x {item.kode_menu.nama_menu_lengkap}, {harga_menu.size.nama_size}'
        menu_price = f'Price: Rp.{harga_menu.harga_menu}'  # Add this line to display the price
        p.drawString(100, y, menu_description)
        y -= 20
        p.drawString(120, y, menu_price)  # Display the price
        y -= 20

    # Add the "Total Penjualan" after menu items
    y -= 20
    p.drawString(100, y, f'Total Penjualan: Rp.{order.total_penjualan}')

    y -= 20
    p.drawString(100, y, f'Kembalian : Rp.{order.kembalian}')
    # Close the PDF object cleanly and finalize the buffer.
    p.showPage()
    p.save()

    # FileResponse to send the PDF as a response
    pdf_data = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.kode_penjualan_faktur}.pdf"'
    response.write(pdf_data)

    return response




@login_required
@role_required(allowed_roles=('kasir','admin'))
def kasiran(request):
     if request.user.userprofile.role != 'kasir':
            
            return redirect('login_view')
     return render(request, 'Kasir/kasiran.html')

@login_required
@role_required(allowed_roles=('kasir','admin'))
def pesanan(request):
    if request.user.userprofile.role != 'kasir':
        return redirect('login_view')

    # Retrieve both completed and pending PenjualanFaktur instances
    completed_orders = PenjualanFaktur.objects.filter(status_lunas=True)
    pending_orders = PenjualanFaktur.objects.filter(status_lunas=False)

# Modify the code in your view to access the size correctly
    for order in completed_orders:
        order.menu_items = PenjualanDetail.objects.filter(nomor_nota_penjualan=order.nomor_nota_penjualan)
        for item in order.menu_items:
            # Get the related HargaMenu based on the harga_menu attribute
            harga_menu = HargaMenu.objects.get(menu=item.kode_menu, harga_menu=item.harga_menu)
            # Access the size through the harga_menu relationship
            item.size = harga_menu.size.nama_size

    for order in pending_orders:
        order.menu_items = PenjualanDetail.objects.filter(nomor_nota_penjualan=order.nomor_nota_penjualan)
        for item in order.menu_items:
            # Get the related HargaMenu based on the harga_menu attribute
            harga_menu = HargaMenu.objects.get(menu=item.kode_menu, harga_menu=item.harga_menu)
            # Access the size through the harga_menu relationship
            item.size = harga_menu.size.nama_size
            
    context = {
        'completed_orders': completed_orders,
        'pending_orders': pending_orders,
    }
    return render(request, 'kasir/pesanan.html', context)

@login_required
@role_required(allowed_roles=('kasir','admin'))
def tabelKasir(request):
     if request.user.userprofile.role != 'kasir':
            return redirect('login_view')
     return render(request, 'kasir/tabelKasir.html')

@login_required
@role_required(allowed_roles=('kasir','admin'))
def update_order(request, order_id):
    if request.user.userprofile.role != 'kasir':
        return redirect('login_view')

    order = get_object_or_404(PenjualanFaktur, id=order_id)

    if request.method == 'POST':
        pembayaran = Decimal(request.POST.get('pembayaran', 0))
        status_lunas = int(request.POST.get('status_lunas', 0))

        kembalian = order.total_penjualan - pembayaran
        order.kembalian = abs(kembalian)

        order.pembayaran = pembayaran
        order.status_lunas = 1  # Update the status based on the form input

        order.save()
        return redirect('pesanan')

    return render(request, 'kasir/pesanan.html', {'order': order})

# 


@login_required
@role_required(allowed_roles=('kasir','admin'))
def cancel_order(request, order_id):
     if request.user.userprofile.role != 'kasir':
        return redirect('login_view')
     
     order = get_object_or_404(PenjualanFaktur, id=order_id)

     if request.method == 'POST':
          
        order.status_lunas = 0

        order.save()
        return redirect('pesanan')
     return render(request, 'kasir/pesanan.html', {'order': order})

@login_required
@role_required(allowed_roles=('kasir','admin'))
def delete_order(request, order_id):
    if request.user.userprofile.role != 'kasir':
        return redirect('login_view')

    # Get the PenjualanFaktur instance to delete
    order = get_object_or_404(PenjualanFaktur, id=order_id)

    if request.method == 'POST':
        # Delete associated PenjualanDetail records
        PenjualanDetail.objects.filter(nomor_nota_penjualan=order.nomor_nota_penjualan).delete()
        
        # Delete the PenjualanFaktur (order) instance
        order.delete()

        # Redirect to a relevant page (e.g., pesanan or a confirmation page)
        return redirect('pesanan')

    # Handle GET request or any other logic if needed
    return render(request, 'kasir/pesanan.html', {'order': order})

     

