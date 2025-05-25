from enum import Enum as E

class UserRoleEnum(E):
    ADMIN = "admin"
    CONTRIBUTOR = 'contributor'
    READER = "reader"

class UserProjectRoleEnum(E):
    PROJECT_ADMI = "project_admin"
    PROJECT_CONTRIBUTOR = 'project_contributor'
    PROJECT_READER = "project_reader"