
document.addEventListener("DOMContentLoaded", function () {
    const gameSelect = document.getElementById("id_game");
    const teamsSelect = document.getElementById("id_teams");
    const teamsContainer = document.getElementById("teams-checkboxes");

    if (!gameSelect || !teamsSelect || !teamsContainer) {
        return;
    }

    function renderTeams() {
        teamsContainer.innerHTML = "";

        const options = Array.from(teamsSelect.options);

        if (options.length === 0) {
            teamsContainer.innerHTML = `
                <p class="text-muted small mb-0">
                    Brak drużyn dla wybranej gry.
                </p>
            `;
            return;
        }

        options.forEach(function (option) {
            const label = document.createElement("label");
            label.className = "team-tile";

            const checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.value = option.value;
            checkbox.checked = option.selected;

            const name = document.createElement("span");
            name.className = "team-tile-name";
            name.textContent = option.textContent;

            checkbox.addEventListener("change", function () {
                option.selected = checkbox.checked;
            });

            label.appendChild(checkbox);
            label.appendChild(name);

            teamsContainer.appendChild(label);
        });
    }

    async function loadTeams(gameId, preserveSelected = false) {
        const selectedTeams = preserveSelected
            ? Array.from(teamsSelect.selectedOptions).map(option => option.value)
            : [];

        teamsSelect.innerHTML = "";
        teamsContainer.innerHTML = "";

        if (!gameId) {
            teamsContainer.innerHTML = `
                <p class="text-muted small mb-0">
                    Wybierz najpierw grę, aby zobaczyć dostępne drużyny.
                </p>
            `;
            return;
        }

        teamsContainer.innerHTML = `
            <p class="text-muted small mb-0">
                Ładowanie drużyn...
            </p>
        `;

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
                option.selected = selectedTeams.includes(String(team.id));

                teamsSelect.appendChild(option);
            });

            renderTeams();

        } catch (error) {
            console.error(error);

            teamsContainer.innerHTML = `
                <p class="text-danger small mb-0">
                    Nie udało się załadować drużyn. Spróbuj ponownie.
                </p>
            `;
        }
    }

    gameSelect.addEventListener("change", function () {
        loadTeams(this.value, false);
    });

    if (gameSelect.value) {
        loadTeams(gameSelect.value, true);
    } else {
        renderTeams();
    }
});
