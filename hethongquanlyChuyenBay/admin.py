from hethongquanlyChuyenBay import app, db
from hethongquanlyChuyenBay.models import Account, User,  UserRole, Flight,  TicketPrice, SeatClass
from flask import redirect, request
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_login import current_user, logout_user
import utils


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class ProductView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True


class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class LogoutView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        logout_user()

        return redirect('/admin')


class StatsView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        month = request.args.get('month')
        year = request.args.get('year')
        sales_starts = utils.sales_stats(month=month, year=year)
        quantity_starts = utils.quantity_stats(month=month, year=year)
        total = utils.total_sales(month=month, year=year)
        return self.render('admin/stats.html',
                           sales_starts=sales_starts, quantity_starts=quantity_starts, total=total, month=month, year=year)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


admin = Admin(app=app, name='QUẢN TRỊ', template_mode='bootstrap4')
admin.add_views(ProductView(Account, db.session, name='TÀI KHOẢN'))
admin.add_views(ProductView(User, db.session, name='NGƯỜI DÙNG'))

admin.add_views(ProductView(Flight, db.session, name='CHUYẾN BAY'))
admin.add_views(ProductView(SeatClass, db.session, name='HẠNG VÉ'))
admin.add_views(ProductView(TicketPrice, db.session, name='GIÁ VÉ'))


admin.add_views(LogoutView(name='Đăng Xuất'))
