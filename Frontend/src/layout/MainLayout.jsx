import Navbar from "../components/Navbar/Navbar";
import Sidebar from "../components/Sidebar/Sidebar";

function MainLayout({ children }) {
    return (
        <div className="min-h-screen bg-gray-100">

            <Navbar />

            <div className="flex">

                <Sidebar />

                <main className="flex-1 p-6">
                    {children}
                </main>

            </div>

        </div>
    );
}

export default MainLayout;