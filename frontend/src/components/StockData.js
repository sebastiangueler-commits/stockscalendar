import React, { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, DollarSign, BarChart3, Activity, Target, AlertTriangle } from 'lucide-react';

const StockData = ({ symbol, data }) => {
  const [loading, setLoading] = useState(false);
  const [stockInfo, setStockInfo] = useState(null);

  useEffect(() => {
    if (symbol && data) {
      setStockInfo(data);
    }
  }, [symbol, data]);

  if (!stockInfo) {
    return (
      <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
        <div className="text-center">
          <Activity className="w-8 h-8 text-gray-400 mx-auto mb-2" />
          <p className="text-gray-400">Cargando datos de {symbol}...</p>
        </div>
      </div>
    );
  }

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2
    }).format(value);
  };

  const formatNumber = (value) => {
    if (value >= 1e9) {
      return `${(value / 1e9).toFixed(1)}B`;
    } else if (value >= 1e6) {
      return `${(value / 1e6).toFixed(1)}M`;
    } else if (value >= 1e3) {
      return `${(value / 1e3).toFixed(1)}K`;
    }
    return value.toLocaleString();
  };

  const getChangeColor = (change) => {
    if (change > 0) return 'text-green-400';
    if (change < 0) return 'text-red-400';
    return 'text-gray-400';
  };

  const getChangeIcon = (change) => {
    if (change > 0) return <TrendingUp className="w-4 h-4" />;
    if (change < 0) return <TrendingDown className="w-4 h-4" />;
    return null;
  };

  return (
    <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-white">{symbol}</h3>
        <div className="flex items-center space-x-2">
          {getChangeIcon(stockInfo.change)}
          <span className={`font-bold ${getChangeColor(stockInfo.change)}`}>
            {formatCurrency(stockInfo.price)}
          </span>
        </div>
      </div>

      {/* Price Change */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="bg-gray-700 p-3 rounded-lg">
          <div className="flex items-center justify-between">
            <span className="text-gray-300 text-sm">Cambio</span>
            <span className={`font-bold ${getChangeColor(stockInfo.change)}`}>
              {formatCurrency(stockInfo.change)}
            </span>
          </div>
          <div className="text-xs text-gray-400 mt-1">
            {stockInfo.change_percent ? `${stockInfo.change_percent.toFixed(2)}%` : 'N/A'}
          </div>
        </div>
        <div className="bg-gray-700 p-3 rounded-lg">
          <div className="flex items-center justify-between">
            <span className="text-gray-300 text-sm">Volumen</span>
            <span className="font-bold text-white">
              {formatNumber(stockInfo.volume)}
            </span>
          </div>
        </div>
      </div>

      {/* Technical Indicators */}
      <div className="mb-6">
        <h4 className="text-lg font-semibold text-white mb-3 flex items-center">
          <BarChart3 className="w-5 h-5 mr-2" />
          Indicadores Técnicos
        </h4>
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-gray-700 p-3 rounded-lg">
            <div className="text-sm text-gray-300">RSI</div>
            <div className="text-lg font-bold text-white">
              {stockInfo.rsi ? stockInfo.rsi.toFixed(1) : 'N/A'}
            </div>
            <div className="text-xs text-gray-400">
              {stockInfo.rsi > 70 ? 'Sobrecomprado' : stockInfo.rsi < 30 ? 'Sobreventa' : 'Normal'}
            </div>
          </div>
          <div className="bg-gray-700 p-3 rounded-lg">
            <div className="text-sm text-gray-300">SMA 20</div>
            <div className="text-lg font-bold text-white">
              {stockInfo.sma_20 ? formatCurrency(stockInfo.sma_20) : 'N/A'}
            </div>
          </div>
          <div className="bg-gray-700 p-3 rounded-lg">
            <div className="text-sm text-gray-300">SMA 50</div>
            <div className="text-lg font-bold text-white">
              {stockInfo.sma_50 ? formatCurrency(stockInfo.sma_50) : 'N/A'}
            </div>
          </div>
          <div className="bg-gray-700 p-3 rounded-lg">
            <div className="text-sm text-gray-300">Rango</div>
            <div className="text-lg font-bold text-white">
              {stockInfo.high && stockInfo.low ? 
                `${formatCurrency(stockInfo.low)} - ${formatCurrency(stockInfo.high)}` : 'N/A'}
            </div>
          </div>
        </div>
      </div>

      {/* Fundamental Data */}
      <div className="mb-6">
        <h4 className="text-lg font-semibold text-white mb-3 flex items-center">
          <DollarSign className="w-5 h-5 mr-2" />
          Datos Fundamentales
        </h4>
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-gray-700 p-3 rounded-lg">
            <div className="text-sm text-gray-300">P/E Ratio</div>
            <div className="text-lg font-bold text-white">
              {stockInfo.pe_ratio ? stockInfo.pe_ratio.toFixed(1) : 'N/A'}
            </div>
            <div className="text-xs text-gray-400">
              {stockInfo.pe_ratio < 15 ? 'Subvaluado' : stockInfo.pe_ratio > 25 ? 'Sobrevaluado' : 'Normal'}
            </div>
          </div>
          <div className="bg-gray-700 p-3 rounded-lg">
            <div className="text-sm text-gray-300">Market Cap</div>
            <div className="text-lg font-bold text-white">
              {stockInfo.market_cap ? formatNumber(stockInfo.market_cap) : 'N/A'}
            </div>
          </div>
          <div className="bg-gray-700 p-3 rounded-lg">
            <div className="text-sm text-gray-300">ROE</div>
            <div className="text-lg font-bold text-white">
              {stockInfo.roe ? `${(stockInfo.roe * 100).toFixed(1)}%` : 'N/A'}
            </div>
          </div>
          <div className="bg-gray-700 p-3 rounded-lg">
            <div className="text-sm text-gray-300">Debt/Equity</div>
            <div className="text-lg font-bold text-white">
              {stockInfo.debt_equity ? stockInfo.debt_equity.toFixed(2) : 'N/A'}
            </div>
          </div>
        </div>
      </div>

      {/* Signal Analysis */}
      {stockInfo.confidence && (
        <div className="mb-6">
          <h4 className="text-lg font-semibold text-white mb-3 flex items-center">
            <Target className="w-5 h-5 mr-2" />
            Análisis de Señal
          </h4>
          <div className="bg-gray-700 p-4 rounded-lg">
            <div className="flex items-center justify-between mb-2">
              <span className="text-gray-300">Confianza</span>
              <span className={`font-bold text-lg ${
                stockInfo.confidence > 0.7 ? 'text-green-400' : 
                stockInfo.confidence > 0.5 ? 'text-yellow-400' : 'text-red-400'
              }`}>
                {(stockInfo.confidence * 100).toFixed(1)}%
              </span>
            </div>
            <div className="w-full bg-gray-600 rounded-full h-2">
              <div 
                className={`h-2 rounded-full ${
                  stockInfo.confidence > 0.7 ? 'bg-green-400' : 
                  stockInfo.confidence > 0.5 ? 'bg-yellow-400' : 'bg-red-400'
                }`}
                style={{ width: `${stockInfo.confidence * 100}%` }}
              ></div>
            </div>
            <div className="mt-2 text-sm text-gray-300">
              {stockInfo.reason || 'Análisis basado en datos técnicos y fundamentales'}
            </div>
          </div>
        </div>
      )}

      {/* Price Targets */}
      {stockInfo.target_price && stockInfo.stop_loss && (
        <div>
          <h4 className="text-lg font-semibold text-white mb-3">Objetivos de Precio</h4>
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-green-900/20 border border-green-500/30 p-3 rounded-lg">
              <div className="text-sm text-green-300">Objetivo</div>
              <div className="text-lg font-bold text-green-400">
                {formatCurrency(stockInfo.target_price)}
              </div>
            </div>
            <div className="bg-red-900/20 border border-red-500/30 p-3 rounded-lg">
              <div className="text-sm text-red-300">Stop Loss</div>
              <div className="text-lg font-bold text-red-400">
                {formatCurrency(stockInfo.stop_loss)}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Data Source */}
      <div className="mt-4 pt-4 border-t border-gray-600">
        <div className="flex items-center justify-between text-xs text-gray-400">
          <span>Última actualización: {new Date().toLocaleTimeString()}</span>
          <span>Fuente: Yahoo Finance + Alpha Vantage</span>
        </div>
      </div>
    </div>
  );
};

export default StockData;
