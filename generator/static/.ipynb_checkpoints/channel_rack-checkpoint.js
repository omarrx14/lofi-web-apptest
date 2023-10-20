// channel_rack.js

document.addEventListener("DOMContentLoaded", function() {
    const channelsData = [
        { name: '808 Kick', grid: '10100101' },
        { name: '808 Clap', grid: '01010101' },
        // ... puedes añadir más canales aquí
    ];

    const rackContainer = document.querySelector(".rack-container");

    channelsData.forEach(channel => {
        const channelDiv = document.createElement("div");
        channelDiv.className = "channel";

        const channelName = document.createElement("span");
        channelName.innerText = channel.name;

        const gridDiv = document.createElement("div");
        gridDiv.className = "grid";
        for(let i = 0; i < channel.grid.length; i++) {
            const gridCell = document.createElement("span");
            gridCell.className = channel.grid[i] === '1' ? 'active' : 'inactive';
            gridDiv.appendChild(gridCell);
        }

        channelDiv.appendChild(channelName);
        channelDiv.appendChild(gridDiv);
        rackContainer.appendChild(channelDiv);
    });
});
