const apiKey = "https://api.open-meteo.com/v1/forecast";
const searchBtn = document.getElementById("search");
const resultDiv = document.getElementById("result");

searchBtn.addEventListener("click", getWeather);

async function getWeather() {
    const city = document.getElementById("city").value.trim();

    if (!city) {
        showMessage("Please enter a city name.");
        return;
    }

    showMessage("Fetching weather... ⏳");

    try {
        // 1. GET city coordinates from geocoding API
        const geoURL = `https://geocoding-api.open-meteo.com/v1/search?name=${city}&count=1`;
        const geoResponse = await fetch(geoURL);
        const geoData = await geoResponse.json();

        if (!geoData.results || geoData.results.length === 0) {
            showMessage("City not found ❌");
            return;
        }

        const { latitude, longitude, name, country } = geoData.results[0];

        // 2. Fetch weather using coordinates
        const weatherURL =
            `${apiKey}?latitude=${latitude}&longitude=${longitude}&current_weather=true`;

        const weatherResponse = await fetch(weatherURL);
        const weatherData = await weatherResponse.json();

        const weather = weatherData.current_weather;

        // 3. Show Weather
        resultDiv.innerHTML = `
            <h2>${name}, ${country}</h2>
            <p><strong>Temperature:</strong> ${weather.temperature}°C</p>
            <p><strong>Windspeed:</strong> ${weather.windspeed} km/h</p>
            <p><strong>Weather Code:</strong> ${weather.weathercode}</p>
            <p class="hint">Updated: ${weather.time}</p>
        `;
    } catch (error) {
        showMessage("Something went wrong. Try again ❗");
        console.log(error);
    }
}

function showMessage(msg) {
    resultDiv.innerHTML = `<p class="hint">${msg}</p>`;
}
