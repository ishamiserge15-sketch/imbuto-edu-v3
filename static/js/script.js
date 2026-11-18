/* ====================================
   IMBUTO EDU - JAVASCRIPT PART 1
   BASIC INTERACTIVITY
==================================== */

/* =========================
   MOBILE MENU TOGGLE
========================= */

// Get elements
const nav = document.querySelector("nav ul");
const menuToggle = document.createElement("div");

// Create menu button dynamically
menuToggle.innerHTML = "☰";
menuToggle.style.fontSize = "28px";
menuToggle.style.cursor = "pointer";
menuToggle.style.color = "white";

// Add it to navbar
const navbar = document.querySelector("nav");
navbar.prepend(menuToggle);

// Toggle menu on click
menuToggle.addEventListener("click", () => {
    nav.classList.toggle("active");
});


/* =========================
   SMOOTH SCROLL FOR LINKS
========================= */

document.querySelectorAll("nav ul li a").forEach(link => {
    link.addEventListener("click", function (e) {
        const targetId = this.getAttribute("href");

        if (targetId.startsWith("#")) {
            e.preventDefault();

            const target = document.querySelector(targetId);

            if (target) {
                window.scrollTo({
                    top: target.offsetTop - 70,
                    behavior: "smooth"
                });
            }
        }
    });
});


/* =========================
   SIMPLE BUTTON FEEDBACK
========================= */

document.querySelectorAll("button").forEach(btn => {
    btn.addEventListener("click", () => {
        btn.style.transform = "scale(0.95)";

        setTimeout(() => {
            btn.style.transform = "scale(1)";
        }, 150);
    });
});/* ====================================
   IMBUTO EDU - JAVASCRIPT PART 2
   SEARCH + DYNAMIC FEATURES
==================================== */

/* =========================
   SEARCH FUNCTIONALITY
========================= */

// Get search elements
const searchInput = document.querySelector(".search-box input");
const searchButton = document.querySelector(".search-box button");

if (searchInput && searchButton) {
    searchButton.addEventListener("click", () => {
        const query = searchInput.value.toLowerCase().trim();

        if (query === "") {
            alert("Please enter something to search.");
            return;
        }

        // Simple demo search logic
        alert("Searching for: " + query);

        // You can later connect this to real school data
    });
}


/* =========================
   FILTER SCHOOL CARDS (BASIC)
========================= */

const schoolCards = document.querySelectorAll(".school-card");

function filterSchools(keyword) {
    schoolCards.forEach(card => {
        const text = card.innerText.toLowerCase();

        if (text.includes(keyword.toLowerCase())) {
            card.style.display = "block";
        } else {
            card.style.display = "none";
        }
    });
}

// Example: live filtering from search input
if (searchInput) {
    searchInput.addEventListener("keyup", () => {
        const value = searchInput.value.trim();

        if (value.length > 0) {
            filterSchools(value);
        } else {
            schoolCards.forEach(card => {
                card.style.display = "block";
            });
        }
    });
}


/* =========================
   DYNAMIC HOVER INFO (CARDS)
========================= */

document.querySelectorAll(".category-card").forEach(card => {
    card.addEventListener("mouseenter", () => {
        card.style.background = "#f0f4ff";
    });

    card.addEventListener("mouseleave", () => {
        card.style.background = "white";
    });
});


/* =========================
   SCROLL REVEAL EFFECT
========================= */

const revealElements = document.querySelectorAll(".school-card, .category-card, .stat-card");

const revealOnScroll = () => {
    const windowHeight = window.innerHeight;

    revealElements.forEach(el => {
        const elementTop = el.getBoundingClientRect().top;

        if (elementTop < windowHeight - 100) {
            el.style.opacity = "1";
            el.style.transform = "translateY(0)";
            el.style.transition = "0.6s ease";
        } else {
            el.style.opacity = "0";
            el.style.transform = "translateY(20px)";
        }
    });
};

window.addEventListener("scroll", revealOnScroll);
revealOnScroll();/* ====================================
   IMBUTO EDU - JAVASCRIPT PART 3
   MINI DATA SYSTEM (SIMULATED DATABASE)
==================================== */

/* =========================
   FAKE SCHOOL DATABASE
========================= */

const schools = [
    {
        name: "Gasabo High School",
        location: "Kigali",
        type: "Academic",
        sports: "Football, Basketball",
        ranking: 1
    },
    {
        name: "Nyamata Secondary School",
        location: "Bugesera",
        type: "Academic",
        sports: "Volleyball",
        ranking: 2
    },
    {
        name: "Rwanda Science Academy",
        location: "Kigali",
        type: "Science & Tech",
        sports: "Athletics",
        ranking: 3
    },
    {
        name: "Elite Sports School",
        location: "Huye",
        type: "Sports",
        sports: "Football, Athletics",
        ranking: 4
    }
];


/* =========================
   RENDER SCHOOLS DYNAMICALLY
========================= */

const schoolGrid = document.querySelector(".school-grid");

function renderSchools(data) {
    if (!schoolGrid) return;

    schoolGrid.innerHTML = "";

    data.forEach(school => {
        const card = document.createElement("div");
        card.classList.add("school-card");

        card.innerHTML = `
            <h3>${school.name}</h3>
            <p><strong>Location:</strong> ${school.location}</p>
            <p><strong>Type:</strong> ${school.type}</p>
            <p><strong>Sports:</strong> ${school.sports}</p>
            <p><strong>Ranking:</strong> #${school.ranking}</p>
            <button>View Details</button>
        `;

        schoolGrid.appendChild(card);
    });
}

// Initial render
renderSchools(schools);


/* =========================
   SMART SEARCH (UPGRADED)
========================= */

function smartSearch(query) {
    const filtered = schools.filter(school => {
        return (
            school.name.toLowerCase().includes(query) ||
            school.location.toLowerCase().includes(query) ||
            school.type.toLowerCase().includes(query) ||
            school.sports.toLowerCase().includes(query)
        );
    });

    renderSchools(filtered);
}


/* =========================
   CONNECT SEARCH INPUT TO DATABASE
========================= */



if (searchInput) {
    searchInput.addEventListener("input", () => {
        const value = searchInput.value.toLowerCase().trim();

        if (value === "") {
            renderSchools(schools);
        } else {
            smartSearch(value);
        }
    });
}


/* =========================
   SORT BY RANKING (OPTIONAL FEATURE)
========================= */

function sortByRanking() {
    const sorted = [...schools].sort((a, b) => a.ranking - b.ranking);
    renderSchools(sorted);
}

// You can call this later from a button if you want/* ====================================
   IMBUTO EDU - JAVASCRIPT PART 4
   FILTER SYSTEM + FINAL FRONTEND LOGIC
==================================== */

/* =========================
   FILTER BY TYPE
========================= */

function filterByType(type) {
    if (type === "all") {
        renderSchools(schools);
        return;
    }

    const filtered = schools.filter(school => {
        return school.type.toLowerCase().includes(type.toLowerCase());
    });

    renderSchools(filtered);
}


/* =========================
   FILTER BY LOCATION
========================= */

function filterByLocation(location) {
    const filtered = schools.filter(school => {
        return school.location.toLowerCase().includes(location.toLowerCase());
    });

    renderSchools(filtered);
}


/* =========================
   FILTER BY SPORTS
========================= */

function filterBySport(sport) {
    const filtered = schools.filter(school => {
        return school.sports.toLowerCase().includes(sport.toLowerCase());
    });

    renderSchools(filtered);
}


/* =========================
   RESET VIEW (SHOW ALL)
========================= */

function resetView() {
    renderSchools(schools);
}


/* =========================
   GLOBAL FILTER SYSTEM (READY FOR BUTTONS)
========================= */

// You can connect these to buttons later in HTML

window.filterByType = filterByType;
window.filterByLocation = filterByLocation;
window.filterBySport = filterBySport;
window.resetView = resetView;


/* =========================
   AUTO HIGHLIGHT ACTIVE FILTER (OPTIONAL UX)
========================= */

const filterButtons = document.querySelectorAll("[data-filter]");

filterButtons.forEach(btn => {
    btn.addEventListener("click", () => {
        filterButtons.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
    });
});
/* ====================================
   IMBUTO EDU - EVENTS & NEWS
   PREMIUM PAGE INTERACTIONS
==================================== */

/* =========================
   PAGE DETECTION
========================= */

const eventsNewsPage =
    document.querySelector(".events-news-header") &&
    document.querySelector(".events-news-section");


/* =========================
   REDUCED MOTION CHECK
========================= */

const reducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
).matches;


/* =========================
   EVENTS & NEWS CARD TILT
========================= */

if (eventsNewsPage && !reducedMotion) {

    const newsCards = document.querySelectorAll(".news-card");

    newsCards.forEach(card => {

        card.addEventListener("mousemove", (event) => {

            // Disable tilt on smaller screens
            if (window.innerWidth <= 900) return;

            const rect = card.getBoundingClientRect();

            const x = event.clientX - rect.left;
            const y = event.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateY =
                ((x - centerX) / centerX) * 2.5;

            const rotateX =
                ((centerY - y) / centerY) * 2.5;

            card.style.transform = `
                perspective(900px)
                translateY(-10px)
                rotateX(${rotateX}deg)
                rotateY(${rotateY}deg)
            `;
        });


        card.addEventListener("mouseleave", () => {

            card.style.transform = "";

        });

    });
}


/* =========================
   HERO POINTER DEPTH
========================= */

if (eventsNewsPage && !reducedMotion) {

    const hero = document.querySelector(
        ".events-news-header"
    );

    if (hero) {

        hero.addEventListener("mousemove", (event) => {

            if (window.innerWidth <= 900) return;

            const rect = hero.getBoundingClientRect();

            const x =
                (event.clientX - rect.left) /
                rect.width -
                0.5;

            const y =
                (event.clientY - rect.top) /
                rect.height -
                0.5;

            const heading =
                hero.querySelector("h1");

            if (heading) {

                heading.style.transform = `
                    translate(
                        ${x * 8}px,
                        ${y * 5}px
                    )
                `;
            }
        });


        hero.addEventListener("mouseleave", () => {

            const heading =
                hero.querySelector("h1");

            if (heading) {
                heading.style.transform = "";
            }

        });

    }
}


/* =========================
   NEWS CARD IMAGE LOAD EFFECT
========================= */

if (eventsNewsPage) {

    const newsImages =
        document.querySelectorAll(".news-card-image");

    newsImages.forEach(image => {

        if (image.complete) {
            image.classList.add("loaded");
        } else {

            image.addEventListener(
                "load",
                () => {
                    image.classList.add("loaded");
                },
                { once: true }
            );

        }

    });
}


/* =========================
   EVENTS PAGE READY STATE
========================= */

if (eventsNewsPage) {

    document.body.classList.add(
        "events-news-page-ready"
    );

}
/* ====================================
   IMBUTO EDU - EVENTS & NEWS
   PHASE 3: ADVANCED MOTION
==================================== */

/* =========================
   TIMELINE + NEWS REVEAL
========================= */

const eventsMotionPage =
    document.querySelector(".events-news-header") &&
    document.querySelector(".events-timeline-section");

const eventsReducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
).matches;


if (eventsMotionPage && !eventsReducedMotion) {

    const motionItems = document.querySelectorAll(
        ".featured-event-card, .news-card, .timeline-item"
    );

    motionItems.forEach((item, index) => {

        item.classList.add("events-motion-item");

        item.style.setProperty(
            "--events-delay",
            `${Math.min(index * 70, 500)}ms`
        );

    });


    const motionObserver = new IntersectionObserver(
        (entries, observer) => {

            entries.forEach(entry => {

                if (entry.isIntersecting) {

                    entry.target.classList.add(
                        "events-motion-visible"
                    );

                    observer.unobserve(entry.target);

                }

            });

        },
        {
            threshold: 0.12,
            rootMargin: "0px 0px -50px 0px"
        }
    );


    motionItems.forEach(item => {
        motionObserver.observe(item);
    });

}


/* =========================
   TIMELINE MARKER MOTION
========================= */

if (eventsMotionPage && !eventsReducedMotion) {

    const timelineItems =
        document.querySelectorAll(".timeline-item");

    const timelineObserver = new IntersectionObserver(
        (entries, observer) => {

            entries.forEach(entry => {

                if (!entry.isIntersecting) return;

                const marker =
                    entry.target.querySelector(
                        ".timeline-marker"
                    );

                if (marker) {
                    marker.classList.add(
                        "timeline-marker-active"
                    );
                }

                observer.unobserve(entry.target);

            });

        },
        {
            threshold: 0.35
        }
    );


    timelineItems.forEach(item => {
        timelineObserver.observe(item);
    });

}


/* =========================
   FEATURED CARD POINTER DEPTH
========================= */

if (eventsMotionPage && !eventsReducedMotion) {

    const featuredCard =
        document.querySelector(".featured-event-card");


    if (featuredCard) {

        featuredCard.addEventListener(
            "mousemove",
            event => {

                if (window.innerWidth <= 900) return;


                const rect =
                    featuredCard.getBoundingClientRect();


                const x =
                    (event.clientX - rect.left) /
                    rect.width -
                    0.5;


                const y =
                    (event.clientY - rect.top) /
                    rect.height -
                    0.5;


                featuredCard.style.transform = `
                    translateY(-8px)
                    perspective(1200px)
                    rotateX(${y * -2}deg)
                    rotateY(${x * 2}deg)
                `;

            }
        );


        featuredCard.addEventListener(
            "mouseleave",
            () => {

                featuredCard.style.transform = "";

            }
        );

    }

}


/* =========================
   TIMELINE HOVER DEPTH
========================= */

if (eventsMotionPage && !eventsReducedMotion) {

    const timelineCards =
        document.querySelectorAll(".timeline-card");


    timelineCards.forEach(card => {

        card.addEventListener(
            "mousemove",
            event => {

                if (window.innerWidth <= 900) return;


                const rect =
                    card.getBoundingClientRect();


                const x =
                    (event.clientX - rect.left) /
                    rect.width -
                    0.5;


                const y =
                    (event.clientY - rect.top) /
                    rect.height -
                    0.5;


                card.style.transform = `
                    translateY(-5px)
                    perspective(800px)
                    rotateX(${y * -1.5}deg)
                    rotateY(${x * 1.5}deg)
                `;

            }
        );


        card.addEventListener(
            "mouseleave",
            () => {

                card.style.transform = "";

            }
        );

    });

}


/* =========================
   EVENTS PAGE READY
========================= */

if (eventsMotionPage) {

    document.body.classList.add(
        "events-news-motion-ready"
    );

}