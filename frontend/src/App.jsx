import { CheckCircleOutlined, MinusCircleOutlined } from "@ant-design/icons"
import { Col, Row, Timeline } from "antd"
import { useEffect, useState } from "react"

function App() {
    const [tasks, setTasks] = useState([])

    useEffect(() => {
        const fetchAllTasks = async () => {
            const response = await fetch("/task/")
            const fetchedTasks = await response.json()
            setTasks(fetchedTasks)
        }

        const interval = setInterval(fetchAllTasks, 1000)

        return () => {
            clearInterval(interval)
        }
    }, [])

    const timelineItems = [...tasks].reverse().map((task) =>
        task.completed
            ? {
                  dot: <CheckCircleOutlined />,
                  color: "green",
                  children: (
                      <span style={{ textDecoration: "line-through", color: "green" }}>
                          {task.name} <small>({task._id})</small>
                      </span>
                  ),
              }
            : {
                  dot: <MinusCircleOutlined />,
                  color: "blue",
                  children: (
                      <span>
                          {task.name} <small>({task._id})</small>
                      </span>
                  ),
              }
    )

    return (
        <>
            <Row style={{ marginTop: 50 }}>
                <Col span={14} offset={5}>
                    <Timeline mode="alternate" items={timelineItems} />
                </Col>
            </Row>
        </>
    )
}

export default App
