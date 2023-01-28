import React, {useState} from "react";
import {Link, useNavigate} from "react-router-dom";
import ValidationErrors from "../../../utilities/ValidationErrors";


const EditAddEmployeeWidget = function(props) {
  const client = props.client;
  const [id, setId] = useState(props.id || null);
  const [name, setName] = useState(props.name || '');
  const [department, setDepartment] = useState(props.department || EMPLOYEE_DEPARTMENT_CHOICES[0].id);
  const [salary, setSalary] = useState(props.salary || '');
  const [errors, setErrors] = useState({});
  const editMode = Boolean(id);
  const navigate = useNavigate();


  const saveEmployee = function() {
    let employee = {
      name: name,
      department: department,
      salary: salary,
    };
    let params = {};
    let apiFunction;
    if (editMode) {
      params['id'] = id;
      params['patchedEmployee'] = employee;
      apiFunction = 'employeesPartialUpdate';
    } else {
      params['employee'] = employee;
      apiFunction = 'employeesCreate';
    }
    client[apiFunction](params).then((result) => {
      props.employeeSaved(result);
      navigate('/');
    }).catch((error) => {
      error.response.json().then((errors) => {
        setErrors(errors);
      })
    });
  };

  return (
    <section className="app-card">
      <h3 className="pg-subtitle">Employee Details</h3>
      <div className="pg-input-group">
        <label className="pg-label">Name</label>
        <input className="pg-control" type="text" placeholder="Michael Scott"
               onChange={(event) => setName(event.target.value)} value={name}>
        </input>
        <p className="pg-help">Your employee's name.</p>
        <ValidationErrors errors={errors.name} />
      </div>
      <div className="mb-3">
        <label className="pg-label">Department</label>
        <div className="pg-select">
          <select onChange={(event) => setDepartment(event.target.value)} value={department}>
            {EMPLOYEE_DEPARTMENT_CHOICES.map(
              (department, index) => <option key={department.id}
                                             value={department.id}>{department.name}</option>
            )}
          </select>
        </div>
        <p className="pg-help">What department your employee belongs to.</p>
        <ValidationErrors errors={errors.department} />
      </div>
      <div className="pg-input-group">
        <label className="pg-label">Salary</label>
        <input className="pg-control" type="number" min="0" placeholder="50000"
               onChange={(event) => setSalary(event.target.value)} value={salary}>
        </input>
        <p className="pg-help">Your employee's annual salary.</p>
        <ValidationErrors errors={errors.salary} />
      </div>
      <div className="pg-inline-buttons">
        <button className={editMode ? 'pg-button-secondary' : 'pg-button-primary'}
                onClick={() => saveEmployee()}>
            <span className="pg-icon">
              <i className={`fa ${editMode ? 'fa-check' : 'fa-plus'}`}></i>
            </span>
          <span>{editMode ? 'Save Employee' : 'Add Employee'}</span>
        </button>
        <Link to="/">
          <button className="pg-button-light mx-2">
            <span>Cancel</span>
          </button>
        </Link>
      </div>
    </section>
  );
};

export default EditAddEmployeeWidget;
