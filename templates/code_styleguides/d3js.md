# D3.js Style Guide

This document outlines coding standards and best practices for D3.js (Data-Driven Documents) visualizations in this project.

## Project Structure and Organization

```
project/
├── src/
│   ├── components/          # Reusable visualization components
│   │   ├── BarChart.js
│   │   ├── LineChart.js
│   │   └── ScatterPlot.js
│   ├── charts/              # Chart-specific implementations
│   │   ├── SalesChart.js
│   │   └── UserGrowthChart.js
│   ├── utils/               # Utility functions
│   │   ├── scales.js
│   │   ├── axes.js
│   │   └── helpers.js
│   ├── styles/              # CSS/SCSS files
│   │   └── charts.css
│   └── index.js             # Main entry point
├── data/                    # Sample/test data
├── tests/                   # Unit tests
└── examples/                # Usage examples
```

## Module Pattern for Reusable Components

Create reusable chart components using the module pattern:

```javascript
function barChart() {
    // Private variables with defaults
    let width = 600;
    let height = 400;
    let margin = { top: 20, right: 30, bottom: 40, left: 50 };
    let xAccessor = d => d.x;
    let yAccessor = d => d.y;
    
    // Main function
    function chart(selection) {
        selection.each(function(data) {
            const svg = d3.select(this)
                .attr('width', width)
                .attr('height', height);
            
            // Implementation here
            update(data);
        });
    }
    
    // Getter/setter methods
    chart.width = function(value) {
        if (!arguments.length) return width;
        width = value;
        return chart;
    };
    
    chart.height = function(value) {
        if (!arguments.length) return height;
        height = value;
        return chart;
    };
    
    chart.margin = function(value) {
        if (!arguments.length) return margin;
        margin = value;
        return chart;
    };
    
    return chart;
}

// Usage
const myChart = barChart()
    .width(800)
    .height(500)
    .margin({ top: 30, right: 40, bottom: 50, left: 60 });

d3.select('#chart')
    .datum(data)
    .call(myChart);
```

## Data Binding (Enter-Update-Exit Pattern)

Always use the enter-update-exit pattern for data binding:

```javascript
function update(data) {
    // Select and bind data
    const bars = svg.selectAll('.bar')
        .data(data, d => d.id); // Use key function for object constancy
    
    // Exit: Remove old elements
    bars.exit()
        .transition()
        .duration(300)
        .attr('y', height)
        .attr('height', 0)
        .remove();
    
    // Enter: Create new elements
    const barsEnter = bars.enter()
        .append('rect')
        .attr('class', 'bar')
        .attr('x', d => xScale(d.category))
        .attr('y', height) // Start from bottom for animation
        .attr('width', xScale.bandwidth())
        .attr('height', 0)
        .attr('fill', d => colorScale(d.category));
    
    // Update: Merge and update all elements
    barsEnter.merge(bars)
        .transition()
        .duration(750)
        .attr('x', d => xScale(d.category))
        .attr('y', d => yScale(d.value))
        .attr('width', xScale.bandwidth())
        .attr('height', d => height - yScale(d.value))
        .attr('fill', d => colorScale(d.category));
}
```

## Scales

### Linear Scales
```javascript
const xScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.value)])
    .range([0, width])
    .nice(); // Round to nice values

const yScale = d3.scaleLinear()
    .domain([0, 100])
    .range([height, 0]);
```

### Ordinal/Band Scales
```javascript
const xScale = d3.scaleBand()
    .domain(data.map(d => d.category))
    .range([0, width])
    .padding(0.1); // 10% padding between bars

const colorScale = d3.scaleOrdinal()
    .domain(['A', 'B', 'C'])
    .range(['#1f77b4', '#ff7f0e', '#2ca02c']);
```

### Time Scales
```javascript
const xScale = d3.scaleTime()
    .domain(d3.extent(data, d => d.date))
    .range([0, width]);
```

### Scale Utilities
```javascript
// Create scale from data
function createScale(data, accessor, range, scaleType = 'linear') {
    const scale = d3[`scale${scaleType.charAt(0).toUpperCase() + scaleType.slice(1)}`]();
    
    if (scaleType === 'band') {
        scale.domain(data.map(accessor))
            .range(range)
            .padding(0.1);
    } else {
        scale.domain(d3.extent(data, accessor))
            .range(range)
            .nice();
    }
    
    return scale;
}
```

## Axes Creation and Formatting

```javascript
function createAxes(svg, xScale, yScale, width, height, margin) {
    const xAxis = d3.axisBottom(xScale)
        .tickSizeOuter(0)
        .tickPadding(10);
    
    const yAxis = d3.axisLeft(yScale)
        .ticks(5)
        .tickFormat(d => `$${d3.format('.2s')(d)}`) // Format as currency
        .tickSizeOuter(0);
    
    // X Axis
    const xAxisGroup = svg.append('g')
        .attr('class', 'axis axis-x')
        .attr('transform', `translate(0, ${height})`)
        .call(xAxis);
    
    xAxisGroup.selectAll('text')
        .attr('transform', 'rotate(-45)')
        .style('text-anchor', 'end');
    
    // X Axis Label
    xAxisGroup.append('text')
        .attr('class', 'axis-label')
        .attr('x', width / 2)
        .attr('y', 40)
        .attr('fill', 'currentColor')
        .style('text-anchor', 'middle')
        .text('Category');
    
    // Y Axis
    const yAxisGroup = svg.append('g')
        .attr('class', 'axis axis-y')
        .call(yAxis);
    
    // Y Axis Label
    yAxisGroup.append('text')
        .attr('class', 'axis-label')
        .attr('transform', 'rotate(-90)')
        .attr('x', -height / 2)
        .attr('y', -40)
        .attr('fill', 'currentColor')
        .style('text-anchor', 'middle')
        .text('Value');
    
    return { xAxisGroup, yAxisGroup };
}
```

## Transitions and Animations

```javascript
// Reusable transition factory
function createTransition(duration = 750, ease = d3.easeCubicInOut) {
    return d3.transition()
        .duration(duration)
        .ease(ease);
}

// Staggered animations
function staggeredUpdate(selection, data) {
    selection.data(data)
        .transition()
        .delay((d, i) => i * 50) // 50ms delay between elements
        .duration(500)
        .attr('y', d => yScale(d.value))
        .attr('height', d => height - yScale(d.value));
}

// Chained transitions
function chainedTransition(element) {
    element
        .transition()
        .duration(500)
        .attr('fill', 'orange')
        .transition()
        .duration(500)
        .attr('fill', 'steelblue');
}
```

## Event Handling

```javascript
function setupInteractions(selection) {
    selection
        .on('mouseenter', function(event, d) {
            d3.select(this)
                .transition()
                .duration(200)
                .attr('opacity', 0.8);
            
            showTooltip(event, d);
        })
        .on('mousemove', function(event, d) {
            moveTooltip(event);
        })
        .on('mouseleave', function(event, d) {
            d3.select(this)
                .transition()
                .duration(200)
                .attr('opacity', 1);
            
            hideTooltip();
        })
        .on('click', function(event, d) {
            event.stopPropagation();
            handleClick(d);
        });
}
```

## Responsive Design Patterns

```javascript
function makeResponsive(svg) {
    const container = svg.node().parentNode;
    const width = container.clientWidth;
    const height = container.clientHeight || width * 0.6;
    
    svg.attr('width', width)
        .attr('height', height)
        .attr('viewBox', `0 0 ${width} ${height}`)
        .attr('preserveAspectRatio', 'xMidYMid meet');
    
    return { width, height };
}

// Resize observer for responsiveness
function observeResize(svg, renderCallback) {
    const resizeObserver = new ResizeObserver(entries => {
        for (let entry of entries) {
            const { width, height } = entry.contentRect;
            renderCallback(width, height);
        }
    });
    
    resizeObserver.observe(svg.node().parentNode);
    
    return () => resizeObserver.disconnect();
}
```

## Color Management

```javascript
// Semantic color schemes
const colorSchemes = {
    categorical: d3.schemeCategory10,
    sequential: d3.interpolateBlues,
    diverging: d3.interpolateRdBu,
    highlight: '#ff6b6b',
    neutral: '#868e96'
};

// Accessible color palette
const accessibleColors = [
    '#1f77b4', // blue
    '#ff7f0e', // orange
    '#2ca02c', // green
    '#d62728', // red
    '#9467bd', // purple
    '#8c564b', // brown
    '#e377c2', // pink
    '#7f7f7f', // gray
    '#bcbd22', // olive
    '#17becf'  // cyan
];

// Color scale with accessibility
function createAccessibleColorScale(domain) {
    return d3.scaleOrdinal()
        .domain(domain)
        .range(accessibleColors);
}
```

## Tooltips

```javascript
function createTooltip() {
    return d3.select('body')
        .append('div')
        .attr('class', 'tooltip')
        .style('position', 'absolute')
        .style('visibility', 'hidden')
        .style('background', 'rgba(0, 0, 0, 0.8)')
        .style('color', 'white')
        .style('padding', '8px 12px')
        .style('border-radius', '4px')
        .style('font-size', '12px')
        .style('pointer-events', 'none')
        .style('z-index', '1000');
}

function showTooltip(event, d, content) {
    const tooltip = d3.select('.tooltip');
    
    tooltip
        .style('visibility', 'visible')
        .html(content(d))
        .style('left', `${event.pageX + 10}px`)
        .style('top', `${event.pageY - 10}px`);
}

function hideTooltip() {
    d3.select('.tooltip')
        .style('visibility', 'hidden');
}
```

## Accessibility

```javascript
function addAccessibilityFeatures(svg, data, config) {
    // Title
    svg.append('title')
        .text(config.title || 'Data Visualization');
    
    // Description
    svg.append('desc')
        .text(config.description || 'Chart showing data trends');
    
    // ARIA labels
    svg.attr('role', 'img')
        .attr('aria-label', config.ariaLabel || 'Data visualization');
    
    // Keyboard navigation
    svg.selectAll('.interactive')
        .attr('tabindex', 0)
        .attr('role', 'button')
        .on('keydown', function(event, d) {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                handleInteraction(d);
            }
        });
    
    // Screen reader text
    data.forEach((d, i) => {
        svg.append('text')
            .attr('class', 'sr-only')
            .text(`${d.category}: ${d.value}`);
    });
}
```

## Testing

```javascript
// Test helper
function createTestContainer() {
    const div = document.createElement('div');
    div.style.width = '600px';
    div.style.height = '400px';
    document.body.appendChild(div);
    return div;
}

// Example test
describe('BarChart', () => {
    let container;
    let chart;
    
    beforeEach(() => {
        container = createTestContainer();
        chart = barChart().width(500).height(300);
    });
    
    afterEach(() => {
        container.remove();
    });
    
    test('renders correct number of bars', () => {
        const data = [{ category: 'A', value: 10 }, { category: 'B', value: 20 }];
        
        d3.select(container)
            .datum(data)
            .call(chart);
        
        const bars = container.querySelectorAll('.bar');
        expect(bars.length).toBe(2);
    });
    
    test('applies correct dimensions', () => {
        const svg = container.querySelector('svg');
        expect(svg.getAttribute('width')).toBe('500');
        expect(svg.getAttribute('height')).toBe('300');
    });
});
```

## Performance Tips

```javascript
// 1. Use canvas for large datasets (>10k points)
function createCanvasChart(data) {
    const canvas = d3.select('canvas')
        .attr('width', width)
        .attr('height', height)
        .node();
    
    const ctx = canvas.getContext('2d');
    
    data.forEach(d => {
        ctx.beginPath();
        ctx.arc(xScale(d.x), yScale(d.y), 2, 0, 2 * Math.PI);
        ctx.fill();
    });
}

// 2. Debounce resize handlers
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 3. Use requestAnimationFrame for smooth animations
function animate() {
    requestAnimationFrame(() => {
        updateChart();
    });
}

// 4. Avoid unnecessary selections
// BAD: Selecting inside loop
// GOOD: Select once, update
```

## Best Practices

1. Use the module pattern for reusable components
2. Always implement enter-update-exit pattern
3. Use meaningful variable names (not single letters)
4. Add transitions for data updates
5. Implement responsive design
6. Add accessibility features (ARIA, keyboard nav)
7. Use semantic color schemes
8. Add tooltips for interactive elements
9. Optimize for performance with large datasets
10. Write unit tests for chart logic
11. Document public APIs with JSDoc
12. Use TypeScript for type safety when possible

**BE CONSISTENT.** When creating visualizations, follow established patterns in the project.

*References:*
- [D3.js Documentation](https://d3js.org/)
- [D3.js Gallery](https://observablehq.com/@d3/gallery)
- [D3.js API Reference](https://github.com/d3/d3/blob/main/API.md)
- [D3.js Patterns](https://leanpub.com/d3patterns)
