import React from "react";

export default function SideNav() {
  return (
    <aside
      className="sidenav navbar navbar-vertical navbar-expand-xs border-0 border-radius-xl my-3 fixed-start ms-3 bg-gradient-dark"
      id="sidenav-main"
    >
      <div className="sidenav-header">
        <i
          className="fas fa-times p-3 cursor-pointer text-white opacity-5 position-absolute end-0 top-0 d-none d-xl-none"
          aria-hidden="true"
          id="iconSidenavbb"
        />
        <a className="navbar-brand m-0" href="/">
          <span className="ms-1 font-weight-bold text-white">Starter App</span>
        </a>
      </div>
      <hr className="horizontal light mt-0 mb-2" />
      <div className="collapse navbar-collapse  w-auto  max-height-vh-100" id="sidenav-collapse-main">
        <ul className="navbar-nav">
          <li className="nav-item">
            <a href="/" className="nav-link ">
              <span className="pg-icon">
                <i className="fa fa-home" />
              </span>
              <span>Dashboard</span>
            </a>
          </li>
          <li className="nav-item">
            <a href="/subscriptions/demo/" className="nav-link ">
              <span className="pg-icon">
                <i className="fa fa-desktop" />
              </span>
              <span>Subscription Demo</span>
            </a>
          </li>
        </ul>
      </div>
    </aside>
  );
}
