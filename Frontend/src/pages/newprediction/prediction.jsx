import { useState } from "react";

import MainLayout from "../../layout/MainLayout";
import api from "../../serviecs/api";
import Loader from "../../components/loader/Loader";

function NewPrediction() {

    const [Patient_id, setPatient_id] = useState("");

    const [result, setResult] = useState(null);

    const [loading, setLoading] = useState(false);

    const [formData, setFormData] = useState({
        HR: "",
        Temp: "",
        MAP: "",
        O2Sat: "",
        Resp: ""
    });


  function handleChange(e) {

    const { name, value } = e.target;

    setFormData({
        ...formData,
        [name]: value === "" ? null : Number(value)
    });

}


    const handleSubmit = async (e) => {

    e.preventDefault();

    setLoading(true);

    try {

        const cleanData = Object.fromEntries(
            Object.entries(formData).filter(
                ([key, value]) => value !== ""
            )
        );

        const response = await api.post(
            `/predict?id=${Patient_id}`,
            cleanData
        );

        setResult(response.data);

    } catch (error) {

        console.error(error);

        console.error(
            "Backend error:",
            error.response?.data
        );

        alert("Prediction Failed");

    } finally {

        setLoading(false);

    }

};

    return (

        <MainLayout>

            <h1 className="text-3xl font-bold mb-6">
                New Prediction
            </h1>


            <form onSubmit={handleSubmit}>

                <div className="grid md:grid-cols-2 gap-6">


                    {/* Patient ID */}

                    <input
                        name="Patient_id"
                        placeholder="Patient ID"
                        value={Patient_id}
                        onChange={(e) => setPatient_id(e.target.value)}
                        className="border p-3 rounded"
                        required
                    />


                    {/* HR */}

                    <input
                        name="HR"
                        placeholder="Heart Rate"
                        value={formData.HR}
                        onChange={handleChange}
                        className="border p-3 rounded"
                    />


                    {/* Temperature */}

                    <input
                        name="Temp"
                        placeholder="Temperature"
                        value={formData.Temp}
                        onChange={handleChange}
                        className="border p-3 rounded"
                    />


                    {/* MAP */}

                    <input
                        name="MAP"
                        placeholder="MAP"
                        value={formData.MAP}
                        onChange={handleChange}
                        className="border p-3 rounded"
                    />


                    {/* O2Sat */}

                    <input
                        name="O2Sat"
                        placeholder="Oxygen Saturation"
                        value={formData.O2Sat}
                        onChange={handleChange}
                        className="border p-3 rounded"
                    />


                    {/* Resp */}

                    <input
                        name="Resp"
                        placeholder="Respiration Rate"
                        value={formData.Resp}
                        onChange={handleChange}
                        className="border p-3 rounded"
                    />

                </div>


                <button
                    type="submit"
                    disabled={loading}
                    className="bg-blue-600 text-white px-6 py-3 rounded mt-8"
                >

                    {loading ? "Predicting..." : "Predict"}

                </button>

            </form>


            {result && (

                <div className="mt-10 bg-white rounded-xl shadow-lg p-6">

                    <h2 className="text-2xl font-bold mb-6">
                        Prediction Result
                    </h2>

                    <div className="space-y-4">

                        <div>

                            <span className="font-semibold">
                                Prediction :
                            </span>

                            {result.prediction === 1 ? (

                                <span className="text-red-600 font-bold">
                                    High Risk
                                </span>

                            ) : (

                                <span className="text-green-600 font-bold">
                                    Low Risk
                                </span>

                            )}

                        </div>


                        <div>

                            <span className="font-semibold">
                                Probability :
                            </span>

                            {result.probability} %

                        </div>


                        <div>

                            <span className="font-semibold">
                                Risk Score :
                            </span>

                            {result.risk_score}

                        </div>

                    </div>

                </div>

            )}

        </MainLayout>

    );

}

export default NewPrediction;