document.addEventListener("DOMContentLoaded", function () {

    loadJobs();
    setupNavbar();

});


/* =========================
   LOAD JOBS
========================= */

async function loadJobs() {

    const jobsContainer =
        document.getElementById("jobsContainer");

    // Profile page par jobs container nahi hai
    if (!jobsContainer) {
        return;
    }

    try {

        const response =
            await fetch("/api/jobs/");

        if (!response.ok) {
            throw new Error("Unable to load jobs");
        }
const data =
    await response.json();


document.getElementById("profileUsername").textContent =
    data.username || "My Profile";

document.getElementById("profileEmail").textContent =
    data.user_email || "";

const username =
    data.username || "U";

document.getElementById("avatarLetter").textContent =
    username.charAt(0).toUpperCase();


document.getElementById("headline").value =
    data.headline || "";

document.getElementById("bio").value =
    data.bio || "";

document.getElementById("location").value =
    data.location || "";

document.getElementById("skills").value =
    data.skills || "";

        const jobs =
            data.results || data;

        if (!jobs.length) {

            jobsContainer.innerHTML = `
                <div class="no-jobs">
                    <h3>No jobs available</h3>

                    <p>
                        There are no published jobs available right now.
                    </p>
                </div>
            `;

            return;
        }

        jobsContainer.innerHTML = "";

        jobs.slice(0, 6).forEach(job => {

            const card =
                document.createElement("div");

            card.className = "job-card";

            card.innerHTML = `

                <div class="company-logo">
                    ${getCompanyInitial(job.company_name)}
                </div>

                <h3>
                    ${escapeHTML(job.title)}
                </h3>

                <p class="company-name">
                    ${escapeHTML(
                        job.company_name || "Company"
                    )}
                </p>

                <div class="job-info">

                    <span>
                        📍 ${escapeHTML(
                            job.location ||
                            "Location not specified"
                        )}
                    </span>

                    <span>
                        💼 ${formatJobType(
                            job.job_type
                        )}
                    </span>

                </div>

                <div class="job-bottom">

                    <strong>
                        ${formatSalary(
                            job.salary_min,
                            job.salary_max
                        )}
                    </strong>

                    <a
                        href="/jobs/${job.id}/"
                        class="view-job"
                    >
                        View →
                    </a>

                </div>
            `;

            jobsContainer.appendChild(card);

        });

    }

    catch (error) {

        console.error(error);

        jobsContainer.innerHTML = `
            <div class="no-jobs">

                <h3>
                    Unable to load jobs
                </h3>

                <p>
                    Please make sure the Django server is running.
                </p>

            </div>
        `;
    }
}


/* =========================
   NAVBAR
========================= */

function setupNavbar() {

    const token =
        localStorage.getItem("access_token");

    const navButtons =
        document.querySelector(".nav-buttons");

    if (!navButtons) {
        return;
    }

    const loginButton =
        navButtons.querySelector(".login-btn");

    if (!loginButton) {
        return;
    }

    if (token) {

        // Sign In → Profile
        loginButton.textContent = "Profile";
        loginButton.href = "/profile/";


        // Prevent duplicate Logout
        if (
            navButtons.querySelector(".logout-btn")
        ) {
            return;
        }


        const logoutButton =
            document.createElement("a");

        logoutButton.href = "#";
        logoutButton.className =
            "login-btn logout-btn";

        logoutButton.textContent =
            "Logout";


        logoutButton.addEventListener(
            "click",
            function (event) {

                event.preventDefault();

                localStorage.removeItem(
                    "access_token"
                );

                localStorage.removeItem(
                    "refresh_token"
                );

                window.location.href =
                    "/login/";

            }
        );


        navButtons.appendChild(
            logoutButton
        );
    }
}


/* =========================
   COMPANY INITIAL
========================= */

function getCompanyInitial(companyName) {

    if (!companyName) {
        return "J";
    }

    return companyName
        .trim()
        .charAt(0)
        .toUpperCase();
}


/* =========================
   JOB TYPE
========================= */

function formatJobType(type) {

    if (!type) {
        return "Job";
    }

    return type
        .replaceAll("_", " ")
        .toLowerCase()
        .replace(
            /\b\w/g,
            letter => letter.toUpperCase()
        );
}


/* =========================
   SALARY
========================= */

function formatSalary(min, max) {

    if (!min && !max) {
        return "Salary not specified";
    }

    if (min && max) {

        return `₹${formatNumber(min)} – ₹${formatNumber(max)}`;

    }

    if (min) {

        return `₹${formatNumber(min)}+`;

    }

    return `Up to ₹${formatNumber(max)}`;
}


/* =========================
   NUMBER
========================= */

function formatNumber(number) {

    return Number(number)
        .toLocaleString("en-IN");
}


/* =========================
   SECURITY
========================= */

function escapeHTML(value) {

    const div =
        document.createElement("div");

    div.textContent =
        value ?? "";

    return div.innerHTML;
}