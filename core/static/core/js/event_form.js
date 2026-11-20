document.addEventListener("DOMContentLoaded", function () {
    const gameSelect = document.getElementById("id_game");
    const teamsSelect = document.getElementById("id_teams");

    if (!gameSelect || !teamsSelect) {
        return;
    }

    async function loadTeams(gameId) {
        teamsSelect.innerHTML = "";

        if (!gameId) {
            return;
        }

        try {
            const response = await fetch(
                `${teamsUrl}?game_id=${encodeURIComponent(gameId)}`
            );

            if (!response.ok) {
                throw new Error("Nie udało się pobrać drużyn.");
            }

            const data = await response.json();

            data.teams.forEach(function (team) {
                const option = document.createElement("option");
                option.value = team.id;
                option.textContent = team.name;
                teamsSelect.appendChild(option);
            });
        } catch (error) {
            console.error(error);
        }
    }

    gameSelect.addEventListener("change", function () {
        loadTeams(this.value);
    });

    if (gameSelect.value) {
        loadTeams(gameSelect.value);
    }
});