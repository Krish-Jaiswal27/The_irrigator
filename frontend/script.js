async function predictIrrigation() {

    const result = document.getElementById("result");

    result.innerText = "Predicting...";

    const payload = {
        Soil_Type: document.getElementById("soilType").value,
        Soil_Moisture: Number(document.getElementById("soilMoisture").value),
        Temperature_C: Number(document.getElementById("temperature").value),
        Humidity: Number(document.getElementById("humidity").value),
        Rainfall_mm: Number(document.getElementById("rainfall").value),
        Sunlight_Hours: Number(document.getElementById("sunlight").value),
        Wind_Speed_kmh: Number(document.getElementById("windSpeed").value),
        Crop_Type: document.getElementById("cropType").value,
        Previous_Irrigation_mm: Number(
            document.getElementById("previousIrrigation").value
        )
    };

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/predict",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            }
        );

        const data = await response.json();

        result.innerText =
            "Recommended Irrigation Level: " +
            data.irrigation_need;

    } catch (error) {

        console.error(error);

        result.innerText =
            "Unable to connect to prediction server.";
    }
}