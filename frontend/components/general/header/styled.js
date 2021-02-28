import styled from 'styled-components';

export const HeaderContainer = styled.header`
    width: 100%;
    height: 100px;
    border-bottom: 1px solid #a63446;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #a63446;
`;

export const Logo = styled.a`
    display: inline-flex;
    align-items: center;
    font-size: 2em;
    font-weight: bold;

    color: #7e1946;
    text-shadow: 0px 2px 2px rgba(255,255,255,0.1);
`;

export const MenuLink = styled.a`
    font-size: 16px;
    border-bottom: 2px ${(props) => (props.active ? 'solid' : 'dashed')} #fceef4;
    color: #fceef4;
    ${(props) => (props.active ? 'opacity: 1;' : '')}

    &:not(:first-child) {
        margin-left: 25px;
    }

    span {
        color: #fbfef9;
    }
`;
