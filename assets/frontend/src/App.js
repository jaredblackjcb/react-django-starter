import { HashRouter as Router, Route, Routes } from "react-router-dom";
import Footer from "./components/Footer";
import SideNav from "./components/SideNav";
import TopNav from "./components/TopNav";
import HomeScreen from "./screens/HomeScreen";

function App() {
  return (
    <div>
      <SideNav />
      <main className="main-content position-relative border-radius-lg ">
        <TopNav />
        <Router>
          <Routes>
            <Route path="/" element={<HomeScreen />} />
          </Routes>
        </Router>
        <Footer />
      </main>
    </div>
  );
}

export default App;
