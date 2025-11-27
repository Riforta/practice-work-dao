import { Component, ReactNode } from 'react';

type Props = { children: ReactNode };
type State = { hasError: boolean; message?: string };

export default class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: any): State {
    return { hasError: true, message: error?.message || String(error) };
  }

  componentDidCatch(error: any, info: any) {
    console.error('Clientes error:', error, info);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="p-6">
          <h2 className="text-lg font-semibold">Error cargando la vista</h2>
          <p className="text-sm text-red-600">{this.state.message}</p>
        </div>
      );
    }
    return this.props.children;
  }
}
