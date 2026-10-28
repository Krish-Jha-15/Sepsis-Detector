import { useState } from "react";
import { Link } from "react-router-dom";

import MainLayout from "../../layout/MainLayout";
import usePatients from "../../hooks/UsePatient";
import RiskBadge from "../../components/RiskBadge/RiskBadge";
import Loader from "../../components/loader/Loader";

function Patients() {

    const { patients, loading } = usePatients();

    const [search, setSearch] = useState("");

    if (loading) {
        return (
            <MainLayout>
                <Loader/>
            </MainLayout>
        );
    }

    const filteredPatients = patients.filter((patient) =>
        patient.Patient_id
            .toLowerCase()
            .includes(search.toLowerCase())
    );

    return (

        <MainLayout>

            <h1 className="text-3xl font-bold mb-6">
                Patients
            </h1>

            <input
                type="text"
                placeholder="Search Patient ID..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="border rounded-lg p-3 mb-6 w-full"
            />

            <table className="w-full bg-white rounded-xl shadow">

                <thead>

                    <tr className="bg-gray-100">

                        <th className="p-4 text-left">Patient ID</th>

                        <th className="p-4 text-left">Records</th>

                        <th className="p-4 text-left">Risk</th>

                        <th className="p-4 text-left">Action</th>

                    </tr>

                </thead>

                <tbody>

                    {filteredPatients.map((patient) => (

                        <tr
                            key={patient.Patient_id}
                            className="border-b hover:bg-gray-50"
                        >

                            <td className="p-4">
                                {patient.Patient_id}
                            </td>

                            <td className="p-4">
                                {patient.total_records}
                            </td>

                            <td className="p-4">
                                <RiskBadge risk={patient.Risk} />
                            </td>

                            <td className="p-4">

                                <Link
                                    to={`/patients/${patient.Patient_id}`}
                                    className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                                >
                                    View
                                </Link>

                            </td>

                        </tr>

                    ))}

                </tbody>

            </table>

        </MainLayout>

    );

}

export default Patients;