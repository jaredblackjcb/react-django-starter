import React, {useState, useEffect} from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Link,
  useParams,
} from "react-router-dom";
import EditAddEmployeeWidget from "./EditAddEmployeeWidget";
import EmployeeTableRow from "./EmployeeTableRow";
import LoadingScreen from "../../../utilities/Loading";
import LoadError from "../../../utilities/LoadError";


const EmptyEmployeeList = function() {
  return (
    <section className="app-card">
      <div className="pg-columns">
        <div className="pg-column-one-third">
          <img className="img-fluid" alt="Nothing Here" src={STATIC_FILES.undraw_empty}/>
        </div>
        <div className="pg-column">
          <h1 className="pg-title">No Employees Yet!</h1>
          <h2 className="pg-subtitle">Create your first employee below to get started.</h2>
          <div className="my-3">
            <Link to="/new">
              <button className="pg-button-primary">
                <span className="pg-icon"><i className="fa fa-plus"></i></span>
                <span>Create Employee</span>
              </button>
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
};

const EmployeeList = function(props) {
  return (
    <section className="app-card">
      <h3 className="pg-subtitle">All Employees</h3>
      <div className='table-responsive'>
        <table className="table pg-table">
          <thead>
          <tr>
            <th className="pg-text-left">Name</th>
            <th className="pg-text-left">Department</th>
            <th className="pg-text-right">Salary</th>
            <th></th>
          </tr>
          </thead>
          <tbody>
          {
            props.employees.map((employee, index) => {
              // https://stackoverflow.com/a/27009534/8207
              return <EmployeeTableRow key={employee.id} index={index} {...employee}
                                       delete={(index) => props.deleteEmployee(index)}
              />;
            })
          }
          </tbody>
        </table>
      </div>
      <Link to="/new">
        <button className="pg-button-primary">
          <span className="pg-icon">
            <i className="fa fa-plus"></i>
          </span>
          <span>Add Employee</span>
        </button>
      </Link>
    </section>
  );
};


const EmployeeApplication = function(props) {
  const [isLoading, setIsLoading] = useState(true);
  const [loadError, setLoadError] = useState(false);
  const [employees, setEmployees] = useState([]);
  const client = props.client;

  useEffect(() => {
    client.employeesList().then((result) => {
      setEmployees(result.results);
      setIsLoading(false);
    }).catch((error) => {
      console.error(error);
      setLoadError(true);
      setIsLoading(false);
    });
  }, []);

  const getEmployeeById = function(id) {
    for (const employee of employees) {
      if (employee.id.toString() === id) {
        return employee;
      }
    }
  };

  const handleEmployeeSaved = function(employee) {
    let found = false;
    const newEmployees = [];
    // find the appropriate item in the list and update in place
    for (let existingEmployee of employees) {
      if (existingEmployee.id === employee.id) {
        newEmployees.push(employee);
        found = true;
      } else {
        newEmployees.push(existingEmployee);
      }
    }
    if (!found) {
      newEmployees.push(employee);
    }
    setEmployees(newEmployees);
  };

  const deleteEmployee = function (index) {
    client.employeesDestroy({id: employees[index].id}).then((result) => {
      const newEmployees = employees.slice(0, index).concat(employees.slice(index + 1));
      setEmployees(newEmployees);
    });
  };

  const RenderEditEmployee = function () {
    let params = useParams();
    if (isLoading) {
      return <LoadingScreen />;
    } else {
      const employeeId = params.employeeId;
      const employee = getEmployeeById(employeeId);
      return (
        <EditAddEmployeeWidget client={client} {...employee} employeeSaved={handleEmployeeSaved}/>
      );
    }
  };

  const getDefaultView = function() {
    if (isLoading) {
      return <LoadingScreen/>
    }
    if (loadError) {
      return <LoadError/>
    }
    if (employees.length === 0) {
      return <EmptyEmployeeList/>;
    } else {
      return <EmployeeList employees={employees} deleteEmployee={deleteEmployee}/>
    }
  };
  return (
    <BrowserRouter basename={props.urlBase}>
      <Routes>
        <Route path="/new" element={<EditAddEmployeeWidget client={client} employeeSaved={handleEmployeeSaved}/>} />
        <Route path="/edit/:employeeId" element={<RenderEditEmployee />} />
        <Route path="/" element={getDefaultView()} />
       </Routes>
    </BrowserRouter>
  );
};


export default EmployeeApplication;
