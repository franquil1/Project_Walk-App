
        // Inicializar el mapa Leaflet
        var map = L.map('map').setView([2.4419, -76.6063], 15); // Coordenadas

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        // Marcador para la ubicación de Django Torre 24
        var marker = L.marker([2.4419, -76.6063]).addTo(map)
            .bindPopup('<b>Django Torre 24</b><br>Ubicación aproximada.')
            .openPopup();


        // Ejemplo de una línea de ruta 
        var latlngs = [
            [2.441922, -76.606270], // Punto de origen
            [2.444521, -76.599980]  // Punto de destino 
        ];
        var polyline = L.polyline(latlngs, {color: 'blue'}).addTo(map);
        map.fitBounds(polyline.getBounds());