from Library1.Provisioning.Provisioning import Provisioning


class Test_team(Provisioning):
 # Test004,test448,test449,test545,test627
   def test004():
       #creatde
       #validate
       #del
        configuration = Provisioning.open_json("TestCases/input.json")
        print(configuration)
        skill_def_id = Provisioning.create_skill_definition(configuration)
        print(skill_def_id)
        # validate ??
   def test448(self):

#if __name__ == '__main__':
   # Test_team.test0005()