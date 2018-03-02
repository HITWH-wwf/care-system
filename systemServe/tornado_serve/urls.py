#coding=utf8
import os
import tornado.web
from tornado_serve.views import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS = {
    "template_path": os.path.join(BASE_DIR, "template_path"),
    "static_path": os.path.join(BASE_DIR, "static"),
    # 'debug':True
    #"debug" : True

}

HANDLERS = [
    (r"/", IndexHandler),
    (r"/index/grow-line", GrowLineHandler),
    (r"/index/grow-bar", GrowBarHandler),
    (r"/index/focus-table", FocusTableHandler),
    (r"/index/change-early-warning-state",ChangeEarlyWarningStateHandler),
    (r"/index/get-early-warning-stu",GetEarlyWarningStuHandler),
    (r"/index/get-stu-warning-history",GetStuWarningHistoryHandler),

    (r"/person/static-info", StaticInfoHandler),
    (r"/person/trip", TripHandler),
    (r"/person/card", CardHandler),
    (r"/person/score", ScoreHandler),
    (r"/person/cancel-focus", CancelFocusHandler),
    (r"/person/add-focus", AddFocusHandler),
    (r"/person/add-event", AddEventHandler),
    (r"/person/get-event", GetEventHandler),
    (r"/person/change-live-status",ChangeLiveStatusHandler),
    (r"/person/change-school-status",ChangeSchoolStatusHandler),
    (r"/person/set-focus-color",SetFocusColorHandler),
    (r"/person/stay-vacation",StayVacationHandler),

    (r"/office/export", ExportHandler),
    (r"/office/suggestion", SuggestionHandler),
    (r"/system/get-total-user-team", GetTotalUserTeamHandler),
    (r"/system/get-one-user-team", GetOneUserTeamHandler),
    (r"/system/set-one-user-team", SetOneUserTeamHandler),
    (r"/system/del-one-user-team", DelOneUserTeamHandler),
    (r"/system/get-total-role-team", GetTotalRoleTeamHandler),
    (r"/system/get-one-role-team", GetOneRoleTeamHandler),
    (r"/system/set-one-role-team", SetOneRoleTeamHandler),
    (r"/system/del-one-role-team", DelOneRoleTeamHandler),
    (r"/system/get-total-user", GetTotalUserHandler),
    (r"/system/get-one-user", GetOneUserHandler),
    (r"/system/set-one-user", SetOneUserHandler),
    (r"/system/del-one-user", DelOneUserHandler),
    (r"/system/add-one-user", AddOneUserHandler),
    (r"/system/add-one-user-team", AddOneUserTeamHandler),
    (r"/system/add-one-role-team", AddOneRoleTeamHandler),
    (r"/system/early-warning-system-set",EarlyWarningSystemSetHandler),

    (r"/data/update-basic", UpdateBasicHandler),
    (r"/data/update-score", UpdateScoreHandler),
    (r"/data/update-focus",UpdateFocusHandler),
    (r"/login/if-pass", LoginIfPassHandler),
    (r"/login/session", LoginSessionHandler),
    (r"/office/get-abnormal-stu",GetAbnormalStuHandler),
    (r"/login/get-user-role",GetUserRoleHandler),
    (r"/login/change-user-pwd",ChangeUserPwdHandler),
    (r"/login/exit-login",ExitLoginHandler),

    (r"/office/get-manager-class",GetManageClassHandler),
    (r"/office/get-stu-by-cost-fixed",GetStuByCostFixedHandler),
    (r"/office/get-stu-by-cost-free",GetStuByCostFreeHandler),
    (r"/office/get-stu-by-sleep-fixed",GetStuBySleepFixedHandler),
    (r"/office/get-stu-by-sleep-free",GetStuBySleepFreeHandler),
    (r"/office/get-stu-by-score-fixed",GetStuByScoreFixedHandler),
    (r"/office/get-stu-by-score-free",GetStuByScoreFreeHandler),
    (r"/office/get-exam-result",GetExamResultHandler)
]

application = tornado.web.Application(
    handlers = HANDLERS,
**SETTINGS)
