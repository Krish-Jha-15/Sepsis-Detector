import { Link } from "react-router-dom";

function Sidebar() {
    return (
        <aside className="w-64 min-h-screen bg-white shadow-md">

            <ul className="p-4 space-y-4">

                <li>
                    <Link to="/" className="hover:text-blue-600">
                        Dashboard
                    </Link>
                </li>

                <li>
                    <Link to="/patients" className="hover:text-blue-600">
                        Patients
                    </Link>
                </li>

                <li>
                    <Link to="/add-patient" className="hover:text-blue-600">
                        Add Patient
                    </Link>
                </li>

                <li>
                    <Link to="/predicts" className="hover:text-blue-600">
                        predict
                    </Link>
                </li>

            </ul>

        </aside>
    );
}

export default Sidebar;