import MainLayout from "../../layout/MainLayout";
import StatCard from "../../components/StatCard/StatCard";
import usePatients from "../../hooks/UsePatient";
import Loader from "../../components/loader/Loader"
function Dashboard() {

    const { patients, loading } = usePatients();
    // print(patients)
    // console.log(patients)
    if (loading) {

        return (
            <MainLayout>
                <Loader/>
            </MainLayout>
        );

    }

    const TotalPatients=patients.length;

    const HighRisk=patients.filter(
        patient=>patient.Risk ==='HIGH'
    ).length;

    const MediumRisk=patients.filter(
        patient=>patient.Risk==='MEDIUM'
    ).length;

    
    const LowRisk=patients.filter(
        patient=>patient.Risk==='LOW'
    ).length;


    return (

        <MainLayout>

            <h1 className="text-3xl font-bold mb-8">
                Dashboard
            </h1>

            <div className="grid grid-cols-4 gap-6">

                <StatCard

                    title="Total Patients"

                    value={patients.length}

                    color="#2563EB"

                />

                
                <StatCard

                    title="High Risk"

                    value={HighRisk}

                    color="#DC2626"

                />

                
                <StatCard

                    title="Medium Patients"

                    value={MediumRisk}

                    color="#F59E0B"

                />

               
                <StatCard

                    title="Low Patients"

                    value={LowRisk}

                    color="#16A34A"

                />

            </div>
            <div className="bg-white rounded-xl shadow-md mt-10 p-6">

                <h2 className="text-2xl font-semibold mb-4">
                    Recent Patients
                </h2>

                <table className="w-full">

                    <thead>

                        <tr className="border-b">

                            <th className="text-left py-3">Patient ID</th>

                            <th className="text-left py-3">Records</th>

                            <th className="text-left py-3">Risk</th>

                        </tr>

                    </thead>

                    <tbody>
                        {patients.map((patient) => (

                            <tr
                                key={patient.Patient_id}
                                className="border-b hover:bg-gray-50"
                            >
                                <td className="py-3">
                                    {patient.Patient_id}
                                </td>

                                <td>
                                    {patient.total_records}
                                </td>

                                <td>
                                    <span
                                        style={{
                                            backgroundColor:
                                                patient.Risk === "HIGH"
                                                    ? "#EF4444"
                                                    : patient.Risk === "MEDIUM"
                                                    ? "#F59E0B"
                                                    : "#22C55E",
                                            color: "white",
                                            padding: "4px 12px",
                                            borderRadius: "9999px",
                                            fontWeight: "600",
                                            display: "inline-block",
                                            minWidth: "70px",
                                            textAlign: "center"
                                        }}
                                    >
                                        {patient.Risk}
                                    </span>
                                </td>

                            </tr>

                        ))}
                    </tbody>

                </table>

            </div>
        </MainLayout>

    );

}

export default Dashboard;