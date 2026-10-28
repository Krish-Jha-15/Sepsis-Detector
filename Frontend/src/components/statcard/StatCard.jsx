function StatCard({ title, value, color }) {
        // console.log(color);
        // console.log(title);

    return (
        
        <div
            className="bg-white rounded-xl shadow-md p-6 border-l-8 hover:shadow-lg transition"
            style={{
    borderLeft: `16px solid ${color}`
}}
        >
            <p className="text-gray-500 text-lg">
                {title}
            </p>

            <h1 className="text-4xl font-bold mt-3">
                {value}
            </h1>
        </div>
    );
}

export default StatCard;