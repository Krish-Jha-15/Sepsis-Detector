import { useState,useEffect } from "react";

import api from "../serviecs/api";

function usePatient_id(id) {
    const [records,setrecords]=useState([]);
    const [loading,setloading]=useState(true);

    useEffect(()=>{
        async function fetchpatient() {
            try{
                const response=await api.get(`/patients/${id}`);
                setrecords(response.data);
            }
            catch(error){
                console.log("Error While Fetching Patient by ID ",error);
            }
            finally{
                setloading(false);
            }
        }
        fetchpatient();
    },[id])
    return {records,loading}
}

export default usePatient_id