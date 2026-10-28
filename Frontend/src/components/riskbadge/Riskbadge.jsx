
function RiskBadge({risk}){
    let begColor='bg-green-500';

    if(risk=='HIGH'){
        begColor='bg-red-500';
    }

    else if(risk=='MEDIUM'){
         begColor='bg-yellow-500' ;  
    }

    return (
        <span
            className={`${begColor} text-white px-3 py-1 rounded-full text-sm font-medium`}
        >
            {risk}
        </span>
    );
}

export default RiskBadge;