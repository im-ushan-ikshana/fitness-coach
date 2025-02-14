import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import Lottie from 'react-lottie';
import sampleAnimation from '../assets/request_message_2.json';
import './customChat.css';

class CustomChat extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      userMessage: '',
      chatHistory: [],
      isLoading: false
    };
  }

  handleMessageChange = (event) => {
    this.setState({ userMessage: event.target.value });
  };

  // Listen for the Enter key to send the message
  handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      this.handleSendMessage();
    }
  };

  handleSendMessage = async () => {
    const { userMessage, chatHistory } = this.state;
    const { sessionId } = this.props; // Get session ID from props

    if (!userMessage.trim()) {
      return;
    }

    if (!sessionId) {
      console.error('Session ID not found. Please ensure that sessionId is passed as a prop.');
      return;
    }

    console.log("Using Session ID:", sessionId);

    // Create a new chat entry with a placeholder for the bot response.
    // The placeholder "LOTTIE_PLACEHOLDER" is used to indicate that a loading animation should appear.
    const newChatEntry = {
      user: userMessage,
      bot: 'LOTTIE_PLACEHOLDER'
    };

    // Immediately update the UI with the user's message and the loading placeholder.
    this.setState({
      chatHistory: [...chatHistory, newChatEntry],
      userMessage: '',
      isLoading: true
    });

    try {
      const response = await fetch(`http://localhost:8000/user-concerns/${sessionId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ concern: userMessage })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();

      if (!data.response) {
        console.error('Invalid API response:', data);
        // Replace the placeholder with an error message
        const updatedChatHistory = [...this.state.chatHistory];
        updatedChatHistory[updatedChatHistory.length - 1].bot = 'Error: Invalid response';
        this.setState({ chatHistory: updatedChatHistory, isLoading: false });
        return;
      }

      // Replace the loading placeholder with the actual response.
      const updatedChatHistory = [...this.state.chatHistory];
      updatedChatHistory[updatedChatHistory.length - 1].bot = data.response;
      this.setState({
        chatHistory: updatedChatHistory,
        isLoading: false
      });
    } catch (error) {
      console.error('Error sending message:', error);
      const updatedChatHistory = [...this.state.chatHistory];
      updatedChatHistory[updatedChatHistory.length - 1].bot = 'Error sending message';
      this.setState({
        chatHistory: updatedChatHistory,
        isLoading: false
      });
    }
  };

  render() {
    const { userMessage, chatHistory } = this.state;

    // Default options for the Lottie animation.
    const defaultOptions = {
      loop: true,
      autoplay: true,
      animationData: sampleAnimation, // Replace with your actual animation data
      rendererSettings: {
        preserveAspectRatio: "xMidYMid slice"
      }
    };

    // Custom markdown components for ReactMarkdown (for links to open in new tab)
    const markdownComponents = {
      a: ({ node, ...props }) => (
        <a {...props} target="_blank" rel="noopener noreferrer" className="markdown-link">
          {props.children}
        </a>
      )
    };

    return (
      <div className="custom-chat">
        <div className="chat-header">
          <h2>Chat with your AI Trainer</h2>
        </div>
        <div className="chat-history">
          {chatHistory.map((chat, index) => (
            <div key={index} className="chat-message">
              <div className="user-message">
                {chat.user}
              </div>
              <div className="bot-response">
                {chat.bot === 'LOTTIE_PLACEHOLDER' ? (
                  <div className="lottie-animation-container">
                    <Lottie options={defaultOptions} height={25} width={100} />
                  </div>
                ) : (
                  <ReactMarkdown 
                    remarkPlugins={[remarkGfm]}
                    rehypePlugins={[rehypeRaw]}
                    components={markdownComponents}
                  >
                    {chat.bot}
                  </ReactMarkdown>
                )}
              </div>
            </div>
          ))}
        </div>
        <div className="chat-input">
          <input
            type="text"
            value={userMessage}
            onChange={this.handleMessageChange}
            onKeyDown={this.handleKeyDown}
            placeholder="Type your message..."
          />
          <button 
            onClick={this.handleSendMessage}
            className="send-button"
          >
            Send
          </button>
        </div>
      </div>
    );
  }
}

export default CustomChat;
