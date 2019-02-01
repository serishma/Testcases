
#from Library.Provisioning.password_policy import PasswordPolicy
from password_policy import PasswordPolicy


class Password_Policy_Test(object):

    # def __init__(self, name):
    #     self.name = name

    def Test009(self, name):
        pp = PasswordPolicy()
        created_pp = pp.create_password_policy(name=name)
        print("created_pp",created_pp)
        print(pp.validate(site=created_pp))

#Test009()