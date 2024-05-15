from flask_admin import AdminIndexView, expose
from flask_cors import cross_origin

class MyAdminIndexView(AdminIndexView):
  @expose("/")
  def index(self):
    admin = self.render("/admin/")
    return admin