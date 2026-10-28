import { useState } from "react";
import MainLayout from "../../layout/MainLayout";
import InputField from "../../components/inputfields/Inputfields";
import api from "../../serviecs/api";

function AddPatient() {

    const [formData, setFormData] = useState({
        Patient_id: "",
        patient_name: "",
        age: "",
        gender: ""
    });

    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {

        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });

    };

    const handleSubmit = async (e) => {

        e.preventDefault();

        setLoading(true);

        try {

            await api.post("/new_patient", formData);

            alert("Patient Added Successfully");

            setFormData({
                Patient_id: "",
                patient_name: "",
                age: "",
                gender: ""
            });

        } catch (error) {

            console.log(error);

            alert("Unable to add patient");

        } finally {

            setLoading(false);

        }

    };

    return (

        <MainLayout>

            <div className="max-w-3xl mx-auto">

                <div className="bg-white shadow-lg rounded-xl p-8">

                    <h1 className="text-3xl font-bold mb-8">

                        Add New Patient

                    </h1>

                    <form
                        onSubmit={handleSubmit}
                        className="space-y-6"
                    >

                        <InputField
                            label="Patient ID"
                            name="Patient_id"
                            value={formData.Patient_id}
                            onChange={handleChange}
                            placeholder="Enter Patient ID"
                            type="text"
                        />

                        <InputField
                            label="Patient Name"
                            name="patient_name"
                            value={formData.patient_name}
                            onChange={handleChange}
                            placeholder="Enter Name"
                            type="text"
                        />

                        <InputField
                            label="Age"
                            name="age"
                            value={formData.age}
                            onChange={handleChange}
                            placeholder="Enter Age"
                        />

                        <div>

                            <label className="block mb-2 font-medium">

                                Gender

                            </label>

                            <select

                                name="gender"

                                value={formData.gender}

                                onChange={handleChange}

                                className="w-full border rounded-lg p-3"

                            >

                                <option value="">Select Gender</option>

                                <option value="Male">Male</option>

                                <option value="Female">Female</option>

                            </select>

                        </div>

                        <div className="flex gap-4">

                            <button

                                type="button"

                                onClick={() =>
                                    setFormData({
                                        Patient_id: "",
                                        patient_name: "",
                                        age: "",
                                        gender: ""
                                    })
                                }

                                className="bg-gray-500 text-white px-6 py-3 rounded"

                            >

                                Clear

                            </button>

                            <button

                                type="submit"

                                disabled={loading}

                                className="bg-blue-600 text-white px-6 py-3 rounded"

                            >

                                {loading ? "Adding..." : "Add Patient"}

                            </button>

                        </div>

                    </form>

                </div>

            </div>

        </MainLayout>

    );

}

export default AddPatient;