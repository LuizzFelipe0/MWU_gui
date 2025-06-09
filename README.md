<h1>Python GUI Frontend - Money With You (MWU)</h1>

<p><strong>Money With You (MWU)</strong> is a desktop Graphical User Interface (GUI) application developed using <strong>Tkinter</strong> to provide a user-friendly frontend for the existing Money With You (MWU) FastAPI backend. This GUI application enables users to interact intuitively with their personal finance data, offering a visual and organized way to manage expenses and track financial behavior.</p>

<p>The MWU GUI focuses on ease of use, allowing users to effortlessly input, categorize, and visualize their financial records. It ensures that users can securely access and manage their own financial data, maintaining the privacy and integrity established by the backend API.</p>

<h2>Core Features</h2>
<ul>
    <li>Expense and Category Management: Intuitive forms for creating, editing, and deleting expenses and categories.</li>
    <li>Recurring Expense Tracking: Dedicated sections to view and manage recurring financial commitments.</li>
    <li>Financial Overview: Visual dashboards and reports to classify and track income vs. spending.</li>
    <li>Data Synchronization: Seamless integration with the MWU FastAPI backend to ensure real-time data consistency.</li>
</ul>

<h2>Key Technologies</h2>
<ul>
    <li>Tkinter: The standard Python interface to the Tcl/Tk GUI toolkit, used for building the desktop application.</li>
    <li>Requests: Python HTTP library for making API calls to the MWU FastAPI backend.</li>
    <li>Pydantic (optional, for frontend validation): Can be used for client-side data validation to mirror backend models.</li>
    <li>Python 3.10+: The core programming language.</li>
</ul>

<h2>Design Principles</h2>
<ul>
    <li>Web-like Folder Structure: Employs a modular and scalable folder structure, inspired by web application design, to separate concerns (e.g., components, pages, services).</li>
    <li>Separation of Concerns: Distinct modules for UI components, page layouts, API interaction logic, and data models.</li>
    <li>Modularity and Reusability: Focus on creating reusable Tkinter components and utility functions to accelerate development and ensure consistency.</li>
    <li>User-Centric Design: Prioritizes a clear, intuitive, and responsive user experience for financial management.</li>
</ul>

<h2>Requirements</h2>
<ul>
    <li>Python 3.10+</li>
    <li>Access to a running instance of the <strong>Money With You (MWU) Backend API</strong>.</li>
    <li>pip (for dependency management)</li>
</ul>