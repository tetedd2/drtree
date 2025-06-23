function updatePrice(priceText) {
    const box = document.getElementById("priceBox");
    box.innerHTML = priceText;
}
container.innerHTML = `
                <h3>📍 ราคาเงาะ ${cityName}</h3>
                <p>🌡️ ราคาทุเรียน: ${temperature}°C</p>
                <p>☁️ ราคามังคุด: ${description}</p>
`;
