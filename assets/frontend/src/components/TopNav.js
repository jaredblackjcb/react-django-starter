import React from "react";

export default function TopNav() {
  return (
    <nav
      className="navbar navbar-main navbar-expand-lg px-0 mx-4 shadow-none border-radius-xl"
      id="navbarBlur"
      navbar-scroll="true"
    >
      <div className="container-fluid py-1 px-3">
        <div className="collapse navbar-collapse mt-sm-0 mt-2 me-md-0 me-sm-4" id="navbar">
          <div className="ms-md-auto pe-md-3 d-flex align-items-center"></div>
          <ul className="navbar-nav  justify-content-end">
            <li className="nav-item d-xl-none ps-3 d-flex align-items-center">
              <a href="/" className="nav-link text-body p-0" id="iconNavbarSidenav">
                <div className="sidenav-toggler-inner">
                  <i className="sidenav-toggler-line" />
                  <i className="sidenav-toggler-line" />
                  <i className="sidenav-toggler-line" />
                </div>
              </a>
            </li>
            <li className="nav-item px-3 d-flex align-items-center">
              <img
                className="navbar-avatar"
                alt="profile"
                src="https://www.gravatar.com/avatar/42a0dd214dc610ef615cbde7aba62291?s=128&d=identicon"
              />
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
}
