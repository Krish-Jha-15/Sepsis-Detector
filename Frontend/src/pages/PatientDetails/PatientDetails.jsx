import { useParams } from 'react-router-dom';

import  MainLayout from '../../layout/MainLayout'
import usePatient_id from '../../hooks/UsePatient_id'
import RiskBadge from '../../components/riskbadge/Riskbadge'
import Loader from '../../components/loader/Loader';
function PatientDetails() {

    const { id } = useParams();

    const { records, loading } = usePatient_id(id);
    console.log(records)
    if (loading) {

        return (
            <MainLayout>
               <Loader/>
            </MainLayout>
        );

    }

    return (

        <MainLayout>

            <h1 className="text-3xl font-bold mb-6">

                Patient {id}

            </h1>

            <table className="w-full bg-white rounded-xl shadow">

                <thead>

                    <tr className="bg-gray-100">

                        <th className="p-4">Time</th>

                        <th className="p-4">Probability</th>

                        <th className="p-4">Prediction</th>

                    </tr>

                </thead>

                <tbody>

                    {records.map((record) => (

                        <tr
                            key={record.id}
                            className="border-b"
                        >

                            <td className="p-4">

                                {new Date(record.created_at).toLocaleString()}

                            </td>

                            <td className="p-4">

                                {record.probability}%

                            </td>

                            <td className="p-4">

                                <RiskBadge
                                    risk={
                                        record.prediction === 1
                                            ? "High"
                                            : "LOW"
                                    }
                                />

                            </td>

                        </tr>

                    ))}

                </tbody>

            </table>

        </MainLayout>

    );

}

export default PatientDetails;