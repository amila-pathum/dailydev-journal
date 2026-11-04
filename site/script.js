async function loadQuotes() {
    const quoteElement = document.getElementById("quote");
    const authorElement = document.getElementById("author");
    const dateElement = document.getElementById("date");
    const historyElement = document.getElementById("history");

    try {
        const response = await fetch("./data/quotes.json");

        if (!response.ok) {
            throw new Error("Unable to load quote history");
        }

        const quotes = await response.json();

        quotes.sort((a, b) => b.date.localeCompare(a.date));

        if (quotes.length === 0) {
            quoteElement.textContent = "No quotes available yet.";
            authorElement.textContent = "";
            historyElement.textContent = "No history yet.";
            return;
        }

        const latest = quotes[0];

        quoteElement.textContent = `"${latest.quote}"`;
        authorElement.textContent = `— ${latest.author}`;
        dateElement.textContent = latest.date;

        historyElement.replaceChildren();

        quotes.slice(1).forEach(item => {
            const card = document.createElement("article");
            card.className = "history-item";

            const date = document.createElement("small");
            date.textContent = item.date;

            const quote = document.createElement("p");
            quote.textContent = `"${item.quote}"`;

            const author = document.createElement("small");
            author.textContent = `— ${item.author}`;

            card.append(date, quote, author);
            historyElement.appendChild(card);
        });

    } catch (error) {
        quoteElement.textContent = "Unable to load today's quote.";
        authorElement.textContent = "";
        historyElement.textContent = "Please try again later.";
        console.error(error);
    }
}

loadQuotes();