export function isValidUsername(username:string):boolean {
    return username.length >= 3 && !username.includes(' ');
  }
  
  export function isValidPassword(password:string):boolean {
    return password.length >= 8;
  }
  