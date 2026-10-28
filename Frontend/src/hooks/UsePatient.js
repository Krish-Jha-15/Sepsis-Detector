import { useEffect, useState } from "react";
import api from "../serviecs/api";

function usePatients() {

    const [patients, setPatients] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {

        async function fetchPatients() {

            try {

                const response = await api.get("/patients");

                setPatients(response.data);

            } catch (error) {
                
                
                console.log("Error fetching patients:", error); 

            } finally {

                setLoading(false);

            }

        }

        fetchPatients();

    }, []);

    return { patients, loading };

}

export default usePatients;