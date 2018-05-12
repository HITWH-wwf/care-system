from tornado_serve.orm import stu_all_aspect_info,MyBaseModel
class GetStuByStudyInfo():
    def entry(self,receiveRequest,queryType=None,waitFilteStuId=None):
        self.requestData = eval(receiveRequest.request.body)

