import React, { useState, useEffect } from 'react';
import { getCampaignDialogs, deleteDialog } from '../api/client';

function DialogHistory({ campaignId }) {
  const [dialogs, setDialogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedDialog, setSelectedDialog] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('last_message'); // 'last_message' | 'messages_count'

  useEffect(() => {
    loadDialogs();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [campaignId]);

  const loadDialogs = async () => {
    try {
      setLoading(true);
      const response = await getCampaignDialogs(campaignId);
      
      const processedDialogs = response.data.map(d => {
        // Извлекаем дату последнего сообщения из контента, если возможно
        let lastMsgDate = new Date(0);
        if (d.messages && d.messages.length > 0) {
          const lastMsg = d.messages[d.messages.length - 1];
          // Если есть поле timestamp или date
          if (lastMsg.date) {
            lastMsgDate = new Date(lastMsg.date);
          } else {
            // Если дата в тексте "[2023-01-01 12:00:00] Text..."
            const dateMatch = lastMsg.content?.match(/^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]/);
            if (dateMatch) {
              lastMsgDate = new Date(dateMatch[1]);
            }
          }
        }
        
        return {
          ...d,
          lastMessageDate: lastMsgDate,
          status: d.status || 'new'
        };
      });
      
      setDialogs(processedDialogs);
    } catch (err) {
      console.error('Error loading dialogs:', err);
    } finally {
      setLoading(false);
    }
  };

  const filteredDialogs = dialogs
    .filter(dialog => {
      if (!searchTerm) return true;
      const term = searchTerm.toLowerCase();
      return (
        dialog.username?.toLowerCase().includes(term) ||
        dialog.user_id.toString().includes(term) ||
        dialog.session_name.toLowerCase().includes(term)
      );
    })
    .sort((a, b) => {
      if (sortBy === 'last_message') {
        return b.lastMessageDate - a.lastMessageDate;
      }
      return b.messages.length - a.messages.length;
    });

  const formatDate = (date) => {
    if (!date || date.getTime() === 0) return '-';
    return date.toLocaleString('ru-RU', {
      day: '2-digit',
      month: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  };
    // TODO: Implement API endpoint for status update
    // await updateDialogStatusApi(campaignId, dialog.session_name, dialog.user_id, status);
    
    // Optimistic update
    setDialogs(dialogs.map(d => 
      (d.session_name === dialog.session_name && d.user_id === dialog.user_id)
        ? { ...d, status }
        : d
    ));
    if (selectedDialog && selectedDialog.session_name === dialog.session_name && selectedDialog.user_id === dialog.user_id) {
      setSelectedDialog({ ...selectedDialog, status });
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'lead': return <span className="badge badge-success">Лид</span>;
      case 'not_lead': return <span className="badge badge-danger">Не лид</span>;
      case 'later': return <span className="badge badge-warning">Потом</span>;
      default: return <span className="badge badge-secondary">Новый</span>;
    }
  };

  const filteredDialogs = dialogs
    .filter(dialog => {
      if (!searchTerm) return true;
      const term = searchTerm.toLowerCase();
      return (
        dialog.username?.toLowerCase().includes(term) ||
        dialog.user_id.toString().includes(term) ||
        dialog.session_name.toLowerCase().includes(term)
      );
    })
    .sort((a, b) => {
      if (sortBy === 'date') {
        // Mock sorting by date since we don't have real dates yet
        return b.messages.length - a.messages.length; 
      }
      return b.messages.length - a.messages.length;
    });

  if (loading) {
    return <div className="loading">Загрузка диалогов...</div>;
  }

  return (
    <div className="dialog-history">
      <div className="card">
        <div className="card-header" style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
          <div style={{display: 'flex', alignItems: 'center', gap: '15px'}}>
            <h2>💬 История диалогов</h2>
            <select 
              value={sortBy} 
              onChange={(e) => setSortBy(e.target.value)}
              style={{padding: '5px', borderRadius: '4px', border: '1px solid #e2e8f0'}}
            >
              <option value="last_message">По новизне</option>
              <option value="messages_count">По кол-ву сообщений</option>
            </select>
          </div>
          <input
            type="text"
            placeholder="Поиск по username, ID..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{width: '300px', padding: '8px', borderRadius: '4px', border: '1px solid #e2e8f0'}}
          />
        </div>

        {filteredDialogs.length === 0 ? (
          <div className="empty-state">
            <p>Нет диалогов</p>
          </div>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Аккаунт</th>
                <th>Пользователь</th>
                <th>Последнее сообщение</th>
                <th>Статус</th>
                <th>Сообщений</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              {filteredDialogs.map(dialog => (
                <tr key={`${dialog.session_name}_${dialog.user_id}`}>
                  <td>{dialog.session_name}</td>
                  <td>
                    <div>{dialog.username ? `@${dialog.username}` : '-'}</div>
                    <div style={{fontSize: '11px', color: '#666'}}>ID: {dialog.user_id}</div>
                  </td>
                  <td style={{fontSize: '13px'}}>{formatDate(dialog.lastMessageDate)}</td>
                  <td>{getStatusBadge(dialog.status)}</td>
                  <td>{dialog.messages.length}</td>
                  <td>
                    <button
                      className="btn-secondary"
                      onClick={() => setSelectedDialog(dialog)}
                      style={{marginRight: '5px'}}
                    >
                      👁
                    </button>
                    <button
                      className="btn-danger"
                      onClick={() => handleDelete(dialog.session_name, dialog.user_id)}
                    >
                      🗑
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Modal для просмотра диалога */}
      {selectedDialog && (
        <div className="modal-overlay" onClick={() => setSelectedDialog(null)}>
          <div className="modal dialog-modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>
                Диалог с {selectedDialog.username ? `@${selectedDialog.username}` : `ID: ${selectedDialog.user_id}`}
              </h3>
              <button onClick={() => setSelectedDialog(null)} style={{background: 'none', border: 'none', fontSize: '24px', cursor: 'pointer'}}>
                ×
              </button>
            </div>
            
            <div className="dialog-messages" style={{maxHeight: '70vh', minHeight: '50vh', overflowY: 'auto'}}>
              {selectedDialog.messages.map((msg, idx) => (
                <div 
                  key={idx} 
                  className={`message ${msg.role}`}
                  style={{
                    padding: '10px 15px',
                    margin: '10px 0',
                    borderRadius: '8px',
                    backgroundColor: msg.role === 'user' ? '#e6f3ff' : '#f0f0f0',
                    marginLeft: msg.role === 'assistant' ? 'auto' : '0',
                    marginRight: msg.role === 'user' ? 'auto' : '0',
                    maxWidth: '80%'
                  }}
                >
                  <div style={{fontWeight: 'bold', marginBottom: '5px', fontSize: '12px', color: '#666'}}>
                    {msg.role === 'user' ? 'Пользователь' : 'Бот'}
                  </div>
                  <div style={{whiteSpace: 'pre-wrap'}}>{msg.content}</div>
                </div>
              ))}
            </div>

            <div className="modal-footer" style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
              <div className="status-actions">
                <button 
                  className={`btn-status ${selectedDialog.status === 'lead' ? 'active' : ''}`}
                  onClick={() => updateDialogStatus(selectedDialog, 'lead')}
                  style={{backgroundColor: '#48bb78', color: 'white', marginRight: '5px'}}
                >
                  Лид
                </button>
                <button 
                  className={`btn-status ${selectedDialog.status === 'not_lead' ? 'active' : ''}`}
                  onClick={() => updateDialogStatus(selectedDialog, 'not_lead')}
                  style={{backgroundColor: '#f56565', color: 'white', marginRight: '5px'}}
                >
                  Не лид
                </button>
                <button 
                  className={`btn-status ${selectedDialog.status === 'later' ? 'active' : ''}`}
                  onClick={() => updateDialogStatus(selectedDialog, 'later')}
                  style={{backgroundColor: '#ecc94b', color: 'white'}}
                >
                  Потом
                </button>
              </div>
              
              <div>
                <button className="btn-secondary" onClick={() => setSelectedDialog(null)} style={{marginRight: '10px'}}>
                  Закрыть
                </button>
                <button 
                  className="btn-danger" 
                  onClick={() => {
                    handleDelete(selectedDialog.session_name, selectedDialog.user_id);
                    setSelectedDialog(null);
                  }}
                >
                  🗑 Удалить
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default DialogHistory;

