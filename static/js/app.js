document.addEventListener('DOMContentLoaded', () => {
    // State management
    const state = {
        currentSection: 'upload-section',
        dataset: null,
        analysisResults: null,
        sessionId: null
    };

    // UI Elements
    const navItems = document.querySelectorAll('.nav-item');
    const sections = document.querySelectorAll('section');
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const pageTitle = document.getElementById('page-title');
    const pageDesc = document.getElementById('page-desc');
    const breadcrumb = document.getElementById('breadcrumb');

    // Section configurations
    const sectionConfigs = {
        'upload-section': { title: 'Connect Your Data Source', desc: 'Upload your dataset to begin automated analysis and intelligent visualization.', breadcrumb: 'Data Source' },
        'preview-section': { title: 'Dataset Overview', desc: 'Review your data structure and quality metrics.', breadcrumb: 'Data Preview' },
        'analysis-section': { title: 'Configure Analysis', desc: 'Select analysis type and visualization preferences.', breadcrumb: 'Configure Analysis' },
        'results-section': { title: 'Visual Analytics', desc: 'Explore your data through intelligent visualizations.', breadcrumb: 'Visualizations' },
        'insights-section': { title: 'AI-Powered Insights', desc: 'Discover patterns and trends identified by machine learning.', breadcrumb: 'AI Insights' }
    };

    // Navigation Logic
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const target = item.getAttribute('data-target');
            if (target) navigateTo(target);
        });
    });

    function navigateTo(sectionId) {
        // Validation: Don't allow navigation to other sections if no data is uploaded
        if (sectionId !== 'upload-section' && !state.dataset) {
            alert('Please upload a dataset first.');
            return;
        }

        // Update active classes
        sections.forEach(s => s.classList.remove('active'));
        navItems.forEach(n => n.classList.remove('active'));

        document.getElementById(sectionId).classList.add('active');
        document.querySelector(`[data-target="${sectionId}"]`).classList.add('active');

        // Update header
        const config = sectionConfigs[sectionId];
        pageTitle.innerText = config.title;
        pageDesc.innerText = config.desc;
        document.getElementById('breadcrumb-current').innerText = config.breadcrumb;

        state.currentSection = sectionId;
    }

    // File Upload Handling
    dropZone.addEventListener('click', () => fileInput.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = 'var(--primary)';
        dropZone.style.background = 'rgba(99, 102, 241, 0.1)';
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.style.borderColor = 'var(--glass-border)';
        dropZone.style.background = 'rgba(255, 255, 255, 0.02)';
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        const files = e.dataTransfer.files;
        if (files.length) handleFileUpload(files[0]);
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) handleFileUpload(e.target.files[0]);
    });

    async function handleFileUpload(file) {
        const formData = new FormData();
        formData.append('file', file);

        // UI Loading state
        dropZone.innerHTML = `<div class="loader"></div><p>Processing ${file.name}...</p>`;

        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.status === 'success') {
                state.dataset = data.summary;
                state.sessionId = data.session_id;
                updatePreviewUI(data.summary);
                navigateTo('preview-section');
            } else {
                throw new Error(data.detail || 'Upload failed');
            }
        } catch (error) {
            console.error('Upload error:', error);
            alert('Error: ' + error.message);
            resetUploadZone();
        }
    }

    function resetUploadZone() {
        dropZone.innerHTML = `
            <i data-lucide="file-up" class="upload-icon"></i>
            <h2>Drag and drop your dataset here</h2>
            <p style="color: var(--text-muted); margin: 1rem 0;">Or click to browse from your computer</p>
            <input type="file" id="file-input" hidden accept=".csv,.xlsx,.xls,.json">
        `;
        lucide.createIcons();
    }

    function updatePreviewUI(summary) {
        // Update Stats
        const statsGrid = document.getElementById('data-stats');
        statsGrid.innerHTML = `
            <div class="stat-card">
                <div class="stat-icon" style="background: rgba(0, 102, 255, 0.1); color: var(--primary);">
                    <i data-lucide="database" style="width: 20px; height: 20px;"></i>
                </div>
                <div class="stat-label">Total Records</div>
                <div class="stat-value">${summary.shape[0].toLocaleString()}</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon" style="background: rgba(0, 201, 167, 0.1); color: var(--secondary);">
                    <i data-lucide="columns" style="width: 20px; height: 20px;"></i>
                </div>
                <div class="stat-label">Features</div>
                <div class="stat-value">${summary.shape[1]}</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon" style="background: rgba(255, 107, 107, 0.1); color: var(--accent);">
                    <i data-lucide="alert-circle" style="width: 20px; height: 20px;"></i>
                </div>
                <div class="stat-label">Missing Values</div>
                <div class="stat-value">${Object.values(summary.missing_values).reduce((a, b) => a + b, 0)}</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon" style="background: rgba(255, 165, 0, 0.1); color: var(--warning);">
                    <i data-lucide="file-type" style="width: 20px; height: 20px;"></i>
                </div>
                <div class="stat-label">Data Types</div>
                <div class="stat-value" style="font-size: 1.1rem;">Mixed</div>
            </div>
        `;
        lucide.createIcons();

        document.getElementById('row-count').innerText = `${summary.shape[0].toLocaleString()} Rows`;

        // Update Table
        const tableContainer = document.getElementById('preview-table');
        const headers = summary.columns;
        const rows = summary.preview;

        let tableHtml = `<table><thead><tr>`;
        headers.forEach(h => tableHtml += `<th>${h}</th>`);
        tableHtml += `</tr></thead><tbody>`;

        rows.forEach(row => {
            tableHtml += `<tr>`;
            headers.forEach(h => {
                const val = row[h];
                tableHtml += `<td>${val === null ? '<span style="color:red">null</span>' : val}</td>`;
            });
            tableHtml += `</tr>`;
        });

        tableHtml += `</tbody></table>`;
        tableContainer.innerHTML = tableHtml;
    }

    // Analysis Execution
    const runBtn = document.getElementById('run-analysis-btn');
    runBtn.addEventListener('click', async () => {
        const analysisType = document.getElementById('analysis-type').value;
        const vizType = document.getElementById('viz-type').value;

        runBtn.disabled = true;
        runBtn.innerHTML = `<i data-lucide="loader-2" class="spin"></i> Analyzing...`;
        lucide.createIcons();

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    type: analysisType,
                    viz: vizType,
                    session_id: state.sessionId
                })
            });

            let data;
            const contentType = response.headers.get("content-type");
            if (contentType && contentType.indexOf("application/json") !== -1) {
                data = await response.json();
            } else {
                const text = await response.text();
                throw new Error(text || 'Server returned an unexpected response format');
            }

            if (data.status === 'success') {
                renderResults(data.analysis);
                navigateTo('results-section');
                generateInsights(data.analysis.insights);
            } else {
                throw new Error(data.message || 'Analysis failed');
            }
        } catch (error) {
            console.error('Analysis error:', error);
            alert('Analytical Error: ' + error.message);
        } finally {
            runBtn.disabled = false;
            runBtn.innerHTML = `<i data-lucide="play"></i> Run Adaptive Analysis`;
            lucide.createIcons();
        }
    });

    function renderResults(analysis) {
        const ctx = document.getElementById('mainChart').getContext('2d');
        const distCtx = document.getElementById('distChart').getContext('2d');

        if (window.mainChartInst) window.mainChartInst.destroy();
        if (window.distChartInst) window.distChartInst.destroy();

        const labels = analysis.chart_data.labels;
        const values = analysis.chart_data.values;
        const vizPref = analysis.viz_preference;

        // Logic to determine primary chart type
        let chartType = 'bar';
        if (vizPref === 'distribution') {
            // If too many unique values, use bar/histogram view instead of pie
            chartType = labels.length > 8 ? 'bar' : 'pie';
        }
        else if (vizPref === 'relational') chartType = 'line';
        else if (vizPref === 'hierarchical') chartType = 'polarArea';
        else if (vizPref === 'categorical') chartType = 'bar';
        else {
            // Auto recommendation
            if (analysis.type === 'prediction' || analysis.type === 'trend') chartType = 'line';
            else if (analysis.type === 'clustering') chartType = 'doughnut';
            else chartType = 'bar';
        }

        window.mainChartInst = new Chart(ctx, {
            type: chartType,
            data: {
                labels: labels,
                datasets: [{
                    label: 'Primary Metric',
                    data: values,
                    borderColor: '#6366f1',
                    backgroundColor: chartType === 'line' ? 'rgba(99, 102, 241, 0.2)' :
                        ['#6366f1', '#ec4899', '#8b5cf6', '#10b981', '#f59e0b'],
                    tension: 0.4,
                    fill: chartType === 'line'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: chartType === 'pie' || chartType === 'polarArea',
                        labels: { color: '#94a3b8' }
                    }
                },
                scales: chartType === 'pie' || chartType === 'polarArea' ? {} : {
                    y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' }, border: { display: false } },
                    x: { grid: { display: false }, border: { display: false } }
                }
            }
        });

        // Distribution chart (Secondary view)
        window.distChartInst = new Chart(distCtx, {
            type: 'doughnut',
            data: {
                labels: labels.slice(0, 3),
                datasets: [{
                    data: values.slice(0, 3),
                    backgroundColor: ['#6366f1', '#ec4899', '#8b5cf6'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'bottom', labels: { color: '#94a3b8' } }
                },
                cutout: '70%'
            }
        });
    }

    function generateInsights(insights) {
        const list = document.getElementById('insights-list');
        list.innerHTML = insights.map(ins => `
            <div class="insight-card">
                <div class="insight-icon">
                    <i data-lucide="sparkles" style="width: 18px; height: 18px;"></i>
                </div>
                <div class="insight-content">
                    <p class="insight-text">${ins.text}</p>
                </div>
            </div>
        `).join('');
        lucide.createIcons();
    }

    // Reset Functionality
    const resetBtn = document.getElementById('reset-btn');
    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            if (confirm('Are you sure you want to clear all data and reset the system?')) {
                state.dataset = null;
                state.analysisResults = null;
                resetUploadZone();
                navigateTo('upload-section');
                location.reload();
            }
        });
    }

    // Export & Sharing Logic
    const exportBtn = document.getElementById('export-pdf-btn');
    if (exportBtn) {
        exportBtn.addEventListener('click', () => {
            window.print();
        });
    }

    const shareBtn = document.getElementById('share-results-btn');
    if (shareBtn) {
        shareBtn.addEventListener('click', () => {
            const url = window.location.href;
            navigator.clipboard.writeText(url).then(() => {
                alert('Analysis link copied to clipboard!');
            });
        });
    }

    // Theme Toggle
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    const html = document.documentElement;

    // Load saved theme or default to light
    const savedTheme = localStorage.getItem('theme') || 'light';
    html.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';

            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
        });
    }

    function updateThemeIcon(theme) {
        if (themeIcon) {
            themeIcon.setAttribute('data-lucide', theme === 'light' ? 'moon' : 'sun');
            lucide.createIcons();
        }
    }
});
