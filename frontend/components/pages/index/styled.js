import styled from 'styled-components';

export const MainContainer = styled.main`
  display: flex;
  flex-direction: column;
  align-items: center;

  form {
    width: 192px;
  }
`;

export const Input = styled.input`
  padding: 5px;
  font-size: 14px;
  border-radius: 5px;
  border: 1px dashed #052639;
  margin-top: 8px;
`;

export const Button = styled.button`
  cursor: pointer;
  border-radius: 20px;
  padding: 10px 15px;
  color: #ffffff;
  background: #0c6291;
  border: none;
  outline: none;
`;

export const SwitchContainer = styled.div`
  width: 500px;
  margin-bottom: 30px;
`;

export const SwitchButton = styled.button`
  width: 50%;
  box-sizing: border-box;
  height: 50px;
  background: ${(props) => (props.active ? '#0C6291' : 'none')};
  color: ${(props) => (props.active ? '#FFFFFF' : '#000000')};
  border: none;
  cursor: pointer;
  outline: none;
`;

export const Tag = styled.button`
  padding: 5px 8px;
  box-sizing: border-box;
  background: ${(props) => (props.active ? '#0C6291' : '#fcf2f1')};
  color: ${(props) => (props.active ? '#FFFFFF' : '#000000')};
  border: none;
  cursor: pointer;
  outline: none;
  margin: 3px 5px;
`;
