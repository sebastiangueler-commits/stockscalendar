import React, { useState, useEffect } from 'react';
import { Calendar, TrendingUp, TrendingDown, Star, Target } from 'lucide-react';

const MonthlyCalendar = ({ calendarData, onSignalClick }) => {
  const [selectedDate, setSelectedDate] = useState(null);
  const [selectedSignal, setSelectedSignal] = useState(null);

  console.log('MonthlyCalendar received calendarData:', calendarData);
  console.log('CalendarData type:', typeof calendarData);
  console.log('CalendarData keys:', calendarData ? Object.keys(calendarData) : 'null');
  console.log('CalendarData days:', calendarData?.days ? Object.keys(calendarData.days) : 'no days');

  // Generar días del mes actual
  const generateDays = () => {
    const days = [];
    const today = new Date();
    const currentMonth = today.getMonth();
    const currentYear = today.getFullYear();
    const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
    
    for (let day = 1; day <= daysInMonth; day++) {
      const date = new Date(currentYear, currentMonth, day);
      const dayStr = day.toString().padStart(2, '0');
      const monthStr = (currentMonth + 1).toString().padStart(2, '0');
      const yearStr = currentYear.toString();
      const fullDate = `${yearStr}-${monthStr}-${dayStr}`;
      
      days.push({
        day: dayStr,
        month: monthStr,
        year: yearStr,
        fullDate: fullDate,
        date: date
      });
    }
    return days;
  };

  const days = generateDays();
  console.log('Generated days:', days.length, 'days');

  const getSignalColor = (type) => {
    return type === 'BUY' ? 'text-green-400' : type === 'SELL' ? 'text-red-400' : 'text-yellow-400';
  };

  const getSignalBgColor = (type) => {
    return type === 'BUY' ? 'bg-green-900/30' : type === 'SELL' ? 'bg-red-900/30' : 'bg-yellow-900/30';
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 90) return 'text-green-400';
    if (confidence >= 80) return 'text-yellow-400';
    return 'text-red-400';
  };

  const handleDayClick = (day) => {
    console.log('Day clicked:', day.fullDate);
    setSelectedDate(day.fullDate);
    setSelectedSignal(null);
  };

  // Obtener todas las señales del día seleccionado
  const getDaySignals = () => {
    if (!selectedDate || !calendarData || !calendarData.days) {
      console.log('No signals available for:', selectedDate);
      return [];
    }
    const dayData = calendarData.days[selectedDate];
    console.log('Day data for', selectedDate, ':', dayData);
    return dayData ? dayData.signals : [];
  };

  const handleSignalClick = (signal) => {
    setSelectedSignal(signal);
    if (onSignalClick) {
      onSignalClick(signal);
    }
  };

  if (!calendarData) {
    return (
      <div className="text-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
        <p className="mt-4 text-gray-400">Loading calendar data...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <Calendar className="h-6 w-6 text-blue-500" />
          <h2 className="text-xl font-bold text-white">Monthly Calendar</h2>
            </div>
        <div className="text-right">
          <p className="text-sm text-gray-400">Total Signals</p>
          <p className="text-2xl font-bold text-blue-500">{calendarData.total_signals || 0}</p>
        </div>
      </div>

      {/* Calendar Grid */}
        <div className="grid grid-cols-7 gap-2">
        {/* Day Headers */}
        {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map((day) => (
          <div key={day} className="text-center py-2 text-sm font-medium text-gray-400">
              {day}
            </div>
          ))}

        {/* Calendar Days */}
        {days.map((day) => {
          const dayData = calendarData.days?.[day.fullDate];
            const hasSignals = dayData && dayData.signals && dayData.signals.length > 0;
          const isToday = day.fullDate === new Date().toISOString().split('T')[0];
          const isWeekend = day.date.getDay() === 0 || day.date.getDay() === 6;

            return (
              <div
              key={day.fullDate}
              onClick={() => !isWeekend && handleDayClick(day)}
              className={`
                relative p-2 text-center rounded-lg cursor-pointer transition-all duration-200
                ${isWeekend ? 'text-gray-600 bg-gray-800/50 cursor-not-allowed' : 'text-white hover:bg-blue-900/30'}
                ${selectedDate === day.fullDate ? 'bg-blue-900/50 ring-2 ring-blue-500' : ''}
                ${isToday ? 'ring-2 ring-green-500' : ''}
              `}
            >
              <span className="text-sm">{day.day}</span>
              
              {/* Signal Indicators */}
              {hasSignals && !isWeekend && (
                <div className="absolute -top-1 -right-1">
                  <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
                      </div>
                    )}
              
              {/* Signal Count */}
              {hasSignals && !isWeekend && (
                <div className="absolute -bottom-1 -right-1">
                  <span className="text-xs bg-red-500 text-white px-1 rounded-full">
                    {dayData.signals.length}
                  </span>
                  </div>
                )}
              </div>
            );
          })}
      </div>

      {/* Selected Day Signals */}
      {selectedDate && (
        <div className="mt-6 p-4 bg-gray-800/50 rounded-lg">
          <h3 className="text-lg font-semibold text-white mb-4">
            Signals for {selectedDate}
          </h3>
          
          {getDaySignals().length > 0 ? (
              <div className="space-y-3">
              {getDaySignals().map((signal) => (
                <div
                  key={signal.id}
                  onClick={() => handleSignalClick(signal)}
                  className="p-3 bg-gray-700/50 rounded-lg cursor-pointer hover:bg-gray-700/70 transition-colors"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className={`w-3 h-3 rounded-full ${getSignalBgColor(signal.signal)}`}></div>
                      <span className="font-medium text-white">{signal.company}</span>
                      <span className={`text-sm font-medium ${getSignalColor(signal.signal)}`}>
                        {signal.signal}
                  </span>
                </div>
                    <div className="text-right">
                      <p className="text-sm text-gray-400">Confidence</p>
                      <p className={`text-sm font-medium ${getConfidenceColor(signal.confidence)}`}>
                        {signal.confidence}%
                      </p>
              </div>
            </div>
            
                  <div className="mt-2 grid grid-cols-3 gap-2 text-xs">
                    <div>
                      <span className="text-gray-400">Price:</span>
                      <span className="text-white ml-1">${signal.price}</span>
                    </div>
                    <div>
                      <span className="text-gray-400">Change:</span>
                      <span className={`ml-1 ${parseFloat(signal.change) >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                        {signal.change}%
                      </span>
                    </div>
            <div>
                      <span className="text-gray-400">Volume:</span>
                      <span className="text-white ml-1">{(signal.volume / 1000).toFixed(0)}K</span>
                </div>
              </div>
            </div>
              ))}
          </div>
          ) : (
            <p className="text-gray-400 text-center py-4">No signals for this day</p>
          )}
        </div>
      )}

      {/* Signal Details Modal */}
      {selectedSignal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-gray-800 p-6 rounded-lg max-w-md w-full mx-4">
            <h3 className="text-lg font-semibold text-white mb-4">Signal Details</h3>
            
            <div className="space-y-3">
              <div>
                <span className="text-gray-400">Company:</span>
                <span className="text-white ml-2">{selectedSignal.company}</span>
              </div>
              <div>
                <span className="text-gray-400">Signal:</span>
                <span className={`ml-2 font-medium ${getSignalColor(selectedSignal.signal)}`}>
                  {selectedSignal.signal}
                </span>
              </div>
              <div>
                <span className="text-gray-400">Confidence:</span>
                <span className={`ml-2 ${getConfidenceColor(selectedSignal.confidence)}`}>
                  {selectedSignal.confidence}%
                </span>
              </div>
              <div>
                <span className="text-gray-400">Price:</span>
                <span className="text-white ml-2">${selectedSignal.price}</span>
          </div>
              <div>
                <span className="text-gray-400">Change:</span>
                <span className={`ml-2 ${parseFloat(selectedSignal.change) >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                  {selectedSignal.change}%
                </span>
          </div>
              <div>
                <span className="text-gray-400">Volume:</span>
                <span className="text-white ml-2">{(selectedSignal.volume / 1000).toFixed(0)}K</span>
          </div>
              <div>
                <span className="text-gray-400">Time:</span>
                <span className="text-white ml-2">{new Date(selectedSignal.timestamp).toLocaleString()}</span>
          </div>
        </div>
            
            <button
              onClick={() => setSelectedSignal(null)}
              className="mt-6 w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg transition-colors"
            >
              Close
            </button>
      </div>
        </div>
      )}
    </div>
  );
};

export default MonthlyCalendar;
