
#include <iostream>
#include <cnoid/PyUtil>
#include <cnoid/EigenTypes>
#include <cnoid/Body>

using namespace boost::python;
using namespace cnoid;

void test()
{
  std::cout << "This is Body Util " << std::endl;
}

VectorXd angleVector(Body& self, VectorXd& angles)
{
  size_t num = self.numJoints();
  for (size_t i = 0; i < num; i++) {
    self.joint(i)->q() = angles[i];
  }
}




BOOST_PYTHON_MODULE(BodyUtil)
{
    boost::python::import("cnoid.Util");
    boost::python::import("cnoid.Body");
    def("test", test);
    def("angleVector", angleVector);
    implicitly_convertible<BodyPtr, ReferencedPtr>();
}
