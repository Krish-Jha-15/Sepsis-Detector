import {BrowserRouter,Routes,Route} from "react-router-dom";

import Dashboard from "../pages/dashboards/Dashboard";
import Patients from "../pages/patients/Patients";
import AddPatient from "../pages/AddPatient/AddPatient";
import PatientDetails from "../pages/PatientDetails/PatientDetails";
import PredictionHistory from "../pages/predictionHistory/PredictionHistory";
import NewPrediction from "../pages/newprediction/prediction"
// import aa from "../pages/patients"
function AppRoute(){
    return(
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/patients" element={<Patients />} />
                <Route path="/patients/:id" element={<PatientDetails />} />
                <Route path="/add-patient" element={<AddPatient />} />
                <Route path="/patientdetails" element={<PatientDetails />} />
                <Route path="/history/:id" element={<PredictionHistory />} />
                <Route path="/predicts" element={<NewPrediction  />}/>
            </Routes>
        </BrowserRouter>
    )
}

export default AppRoute