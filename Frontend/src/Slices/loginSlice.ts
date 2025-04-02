import { createSlice } from '@reduxjs/toolkit';

const loginSlice = createSlice({
  name: 'login',
  initialState: { value: false },
  reducers: {
    update: (state) => { state.value = !state.value; },
  }
});

export const { update } = loginSlice.actions;
export default loginSlice.reducer;
