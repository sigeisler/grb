import './app-header.less'
import React from 'react'
import { Layout, Menu } from 'antd'
import { GithubOutlined } from '@ant-design/icons'
import _ from 'lodash'

const { Header } = Layout;
const { SubMenu } = Menu;

export const AppHeader = ({history}) => {
    const key = _.last(history.location.pathname.split('/'))
    return <Header className="app-header" style={{ position: 'fixed', zIndex: 1, width: '100%' }}>
      <div className="header-wrapper">
        <div className="logo">Graph Robustness Benchmark</div>
        <Menu theme="dark" mode="horizontal" defaultSelectedKeys={['home']} selectedKeys={[key]} style={{float: 'right'}}>
          <Menu.Item key="home" onClick={() => history.push('/home')}>Home</Menu.Item>
          <Menu.Item key="docs" onClick={() => history.push('/docs')}>Docs</Menu.Item>
          <Menu.Item key="datasets" onClick={() => history.push('/datasets')}>Datasets</Menu.Item>
          <SubMenu key="leaderboard" title="Leaderboard" popupOffset={[-20,-2]}>
            {['Citeseer', 'Cora', 'Flickr', 'Reddit', 'AMiner'].map(dataset_name => <Menu.Item
              key={dataset_name.toLowerCase()} onClick={() => history.push(`/leaderboard/${dataset_name.toLowerCase()}`)}
            >{dataset_name}</Menu.Item>)}
          </SubMenu>
          <Menu.Item key="team" onClick={() => { window.location.href = 'http://keg.cs.tsinghua.edu.cn/' }}>Team</Menu.Item>
          <Menu.Item key="github" onClick={() => { window.location.href = 'https://github.com/Stanislas0/grb' }}>Github <GithubOutlined style={{marginLeft: 5, marginRight: 0}}/></Menu.Item>
        </Menu>
      </div>
    </Header>
  }