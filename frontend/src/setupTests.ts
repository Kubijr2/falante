import "@testing-library/jest-dom/vitest";

// jsdom doesn't implement ResizeObserver, which recharts' ResponsiveContainer
// relies on to size charts. A minimal no-op mock is enough for tests — they
// don't need real resize behavior, just for the component not to crash.
class ResizeObserverMock {
  observe() {}
  unobserve() {}
  disconnect() {}
}

global.ResizeObserver = ResizeObserverMock;

// jsdom doesn't implement scrollIntoView either, which the Study Assistant's
// chat panel calls on every new message to keep the latest one in view.
Element.prototype.scrollIntoView = () => {};
