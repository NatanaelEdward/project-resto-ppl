from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .views import PenjualanDetail,BahanMenu,ProfitSummary,HargaMenu

@receiver(post_save, sender=PenjualanDetail)
def create_or_update_profit_summary(sender, instance, created, **kwargs):
    menu = instance.kode_menu

    if created:  # For a new PenjualanDetail instance
        harga_menu_obj = HargaMenu.objects.filter(menu=menu, harga_menu=instance.harga_menu).first()
        if harga_menu_obj:
            size = harga_menu_obj.size
            bahan_details = BahanMenu.objects.filter(menu=menu, size=size)
            total_bersih = sum(bahan.price * instance.qty_menu for bahan in bahan_details)

            total_kotor = instance.jumlah_harga
            total_profit = total_kotor - total_bersih

            # Create ProfitSummary for the PenjualanDetail
            profit_summary = ProfitSummary.objects.create(
                menu=menu,
                pendapatan_bersih=total_bersih,
                pendapatan_kotor=total_kotor,
                profit=total_profit
            )
            # Link the ProfitSummary to the PenjualanDetail
            instance.profit_summary = profit_summary
            instance.save()

@receiver(post_delete, sender=PenjualanDetail)
def delete_profit_summary(sender, instance, **kwargs):
    if instance.profit_summary:
        instance.profit_summary.delete()
