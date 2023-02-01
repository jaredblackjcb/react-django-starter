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
          <li className="nav-item mt-3">
            <h6 className="ps-4 ms-2 text-uppercase text-xs text-white font-weight-bolder opacity-8">Account pages</h6>
          </li>
          <li className="nav-item">
            <a href="/subscriptions/" className="nav-link ">
              <span className="pg-icon">
                <i className="fa fa-repeat" />
              </span>
              <span>Subscription</span>
            </a>
          </li>
          <li className="nav-item">
            <a href="/users/profile/" className="nav-link ">
              <span className="pg-icon">
                <i className="fa fa-user" />
              </span>
              <span>Profile</span>
            </a>
          </li>
          <li className="nav-item">
            <a href="/accounts/password/change/" className="nav-link ">
              <span className="pg-icon">
                <i className="fa fa-unlock-alt" />
              </span>
              <span>Change Password</span>
            </a>
          </li>
          <li className="nav-item">
            <a href="/accounts/logout/" className="nav-link ">
              <span className="pg-icon">
                <i className="fa fa-sign-out" />
              </span>
              <span>Sign out</span>
            </a>
          </li>
        </ul>
      </div>
      <div className="sidenav-footer position-absolute w-100 bottom-0 ">
        <div className="mx-3">
          <a className="btn bg-gradient-primary mt-4 w-100" href="/" type="button">
            Example
          </a>
        </div>
      </div>
    </aside>
  );
}
