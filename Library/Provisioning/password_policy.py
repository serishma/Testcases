#from Library1.Provisioning.base import Base
from base import Base
from time import sleep


class PasswordPolicy(Base):

    def __init__(self, **kwargs):
        super(PasswordPolicy, self).__init__(**kwargs)

    def create_password_policy(self, **kwargs):
        label = "PasswordPolicy.create_password_policy"
        name = kwargs.get("name", None)
        response = self.create_entity(url="PASSWORD_POLICY_URL",
                                      data_frame="password_policy_data",
                                      to_create={"attributes": {"name__s": name}})
        sleep(2)
        if response == 409:
            password_policies = self.get_entities(url="PASSWORD_POLICY_URL", filter_="auxiliaryDataList")
            names = self.lookup_key(field="name__s", data=password_policies)
            try:
                index = names.index(name)
                if index:
                    password_policy = password_policies[0][index]
                    if password_policy:
                        self.delete_password_policy(id_=password_policy.get("id"))
                        sleep(2)

                        # response = self.update_entity(data_frame="password-policy-update", url="PASSWORD_POLICY_URL",
                        #                  to_create={"id": password_policy.get("id"), "attributes": {"status__i": 1}})
                        response = self.create_password_policy(name=name)
                        sleep(2)

            except ValueError as error_:
                self.print_message(message=str(error_),
                                   function=label,
                                  type_="error")

        return response

    def delete_password_policy(self, **kwargs):
        id_ = kwargs.get("id_", None)
        return self.delete_entity(url="PASSWORD_POLICY_URL",
                                  id_=id_)

    def validate(self, **kwargs):
        site = kwargs.get("site",None)
        xpath = kwargs.get("xpath", "PASSWORD_POLICY_XPATH")
        attribute = kwargs.get("attribute", "*")
        id_ = self.condition_response(data=site)
        print("id_", id_)
        return self.validate_xml(xpath=xpath,
                                 id_=id_,
                                 url_key="PASSWORD_POLICY_URL",
                                 xml_lookup="@policyId",
                                 api_lookup="dbId__l",
                                 attribute=attribute)

# test = PasswordPolicy()
# print(test.create_password_policy(name="ravipr2"))