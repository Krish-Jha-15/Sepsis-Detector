function InputField({
    label,
    name,
    type = "number",
    value,
    onChange,
    placeholder
}) {
    return (
        <div className="flex flex-col gap-2">
            <label
                htmlFor={name}
                className="font-medium text-gray-700"
            >
                {label}
            </label>

            <input
                id={name}
                name={name}
                type={type}
                value={value}
                placeholder={placeholder}
                onChange={onChange}
                className="border rounded-lg p-3 focus:ring-2 focus:ring-blue-500 focus:outline-none"
            />
        </div>
    );
}

export default InputField;