import React, { useState, useEffect } from 'react';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import CampaignSettings from './CampaignSettings';
import AccountsManager from './AccountsManager';
import DialogHistory from './DialogHistory';
import ClientsList from './ClientsList';
import CampaignLogs from './CampaignLogs';
import { 
  startCampaign, 
  stopCampaign, 
  deleteCampaign,
  getCampaignStatus 
} from '../api/client';

function CampaignTabs({ campaigns, onUpdate }) {
  // Инициализируем из localStorage если есть, иначе 0
  const [selectedTab, setSelectedTab] = useState(() => {
    const saved = localStorage.getItem('selectedCampaignTab');
    return saved ? parseInt(saved) : 0;
  });
  const [statuses, setStatuses] = useState({});

  // Сохраняем выбранную вкладку при изменении
  const handleTabSelect = (index) => {
    setSelectedTab(index);
    localStorage.setItem('selectedCampaignTab', index);
  };

  useEffect(() => {
    let isMounted = true;
    let timeoutId;

    const fetchStatuses = async () => {
      await loadStatuses();
      if (isMounted) {
        timeoutId = setTimeout(fetchStatuses, 5000);
      }
    };

    fetchStatuses();
    
    return () => {
      isMounted = false;
      if (timeoutId) clearTimeout(timeoutId);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [campaigns]);

  const loadStatuses = async () => {
    const newStatuses = {};
    for (const campaign of campaigns) {
      try {
        const response = await getCampaignStatus(campaign.id);
        newStatuses[campaign.id] = response.data;
      } catch (err) {
        // Тихо игнорируем ошибки сети (502, timeout и т.д.)
        // Сохраняем предыдущий статус если он был
        if (statuses[campaign.id]) {
          newStatuses[campaign.id] = statuses[campaign.id];
        } else {
          // Если предыдущего статуса нет, используем fallback
          newStatuses[campaign.id] = {
            status: campaign.status || 'unknown',
            is_running: false
          };
        }
        
        // Логируем только если это не сетевая ошибка
        if (!err.message?.includes('Network Error') && !err.code?.includes('ERR_NETWORK')) {
        console.error(`Error loading status for ${campaign.id}:`, err);
        }
      }
    }
    setStatuses(newStatuses);
  };

  const handleStart = async (campaignId) => {
    try {
      await startCampaign(campaignId);
      await loadStatuses();
      onUpdate();
    } catch (err) {
      alert('Ошибка запуска кампании: ' + err.message);
    }
  };

  const handleStop = async (campaignId) => {
    try {
      await stopCampaign(campaignId);
      await loadStatuses();
      onUpdate();
    } catch (err) {
      alert('Ошибка остановки кампании: ' + err.message);
    }
  };

  const handleDelete = async (campaignId) => {
    if (!window.confirm('Вы уверены что хотите удалить эту кампанию?')) {
      return;
    }

    try {
      await deleteCampaign(campaignId);
      onUpdate();
    } catch (err) {
      alert('Ошибка удаления кампании: ' + err.message);
    }
  };

  return (
    <Tabs selectedIndex={selectedTab} onSelect={handleTabSelect}>
      <TabList>
        {campaigns.map(campaign => (
          <Tab key={campaign.id}>
            {campaign.name}
            {statuses[campaign.id]?.is_running && (
              <span className="status-indicator running"> ●</span>
            )}
          </Tab>
        ))}
      </TabList>

      {campaigns.map(campaign => {
        const status = statuses[campaign.id];
        const isRunning = status?.is_running || false;

        return (
          <TabPanel key={campaign.id}>
            <div className="campaign-panel">
              {/* Заголовок с кнопками управления */}
              <div className="campaign-header">
                <div className="campaign-info">
                  <h2>{campaign.name}</h2>
                  <span className={`status-badge ${campaign.status}`}>
                    {campaign.status}
                  </span>
                </div>
                <div className="campaign-actions">
                  {isRunning ? (
                    <button 
                      className="btn-danger" 
                      onClick={() => handleStop(campaign.id)}
                    >
                      ⏹ Остановить
                    </button>
                  ) : (
                    <button 
                      className="btn-success" 
                      onClick={() => handleStart(campaign.id)}
                    >
                      ▶ Запустить
                    </button>
                  )}
                  <button 
                    className="btn-danger" 
                    onClick={() => handleDelete(campaign.id)}
                  >
                    🗑 Удалить
                  </button>
                </div>
              </div>

              {/* Внутренние вкладки кампании */}
              <Tabs forceRenderTabPanel={true}>
                <TabList>
                  <Tab>Настройки</Tab>
                  <Tab>Аккаунты</Tab>
                  <Tab>📋 Логи</Tab>
                  <Tab>История диалогов</Tab>
                  <Tab>Обработанные клиенты</Tab>
                </TabList>

                <TabPanel>
                  <CampaignSettings 
                    campaign={campaign} 
                    onUpdate={onUpdate}
                  />
                </TabPanel>

                <TabPanel>
                  <AccountsManager 
                    campaign={campaign} 
                    onUpdate={onUpdate}
                  />
                </TabPanel>

                <TabPanel>
                  <CampaignLogs 
                    campaign={campaign}
                    isRunning={isRunning}
                  />
                </TabPanel>

                <TabPanel>
                  <DialogHistory campaignId={campaign.id} />
                </TabPanel>

                <TabPanel>
                  <ClientsList campaignId={campaign.id} />
                </TabPanel>
              </Tabs>
            </div>
          </TabPanel>
        );
      })}
    </Tabs>
  );
}

export default CampaignTabs;

